import logging, time
import schedule

import PGHandler
import Common
import Utils

pgHandler = PGHandler.PGHandler(Common.DB_URL)

def UpdateInterestInfo(address, interest, totalInterest, productId):
    timestamp = int(time.time())
    pgHandler.InsertNewInterest(address, interest, totalInterest, timestamp, productId)

def GetTodayInterest(address, productId, balance):
    succ, yesterdayInterest = pgHandler.GetLastInterest(address, productId)
    succ, productInfo = pgHandler.GetProductInfo(productId)
    cli = Utils.MakeBankClient()
    newBalance = cli.bank_get_lock_amount(address, productInfo.get("currency"))
    newTotalInterest = newBalance - balance
    newInterest = newTotalInterest - yesterdayInterest

    info = {
        "interest": newInterest,
        "totalInterest": newTotalInterest
    }

    return info

def GetAccountOrderInfos(offset, limit):
    succ, infoList = pgHandler.GetAccountProductList(offset, limit)

    for i in infoList:
        succ, balance = pgHandler.GetBalanceOfAccount(i.get("address"), i.get("product_id"))
        if succ:
            if balance != 0:
                i["balance"] = balance

    return infoList

def CalcInterest():
    offset = 0
    limit = 10

    while(True):
        infos = GetAccountOrderInfos(offset, limit)

        offset += limit

        for i in infos:
            todayInterest = GetTodayInterest(i.get("address"), i.get("product_id"), i.get("balance"))
            UpdateInterestInfo(i.get("address"), todayInterest.get("interest"), todayInterest.get("totalInterest"), i.get("product_id"))

        if len(infos) < limit:
            break

    return

def main():
    logging.basicConfig(filename="eod.log",
                        format="%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        level=logging.DEBUG)

    schedule.every().day.at("01:00").do(CalcInterest)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
