import logging

from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from DataModules import *

class PGHandler():
    def __init__(self, dbUrl):
        self.engine = create_engine(dbUrl)
        self.session = sessionmaker(bind = self.engine)

    def GetAccountProductList(self, offset, limit):
        s = self.session()

        try:
            result = s.query(ViolasBankDepositOrder.product_id, ViolasBankDepositOrder.address).distinct(ViolasBankDepositOrder.product_id, ViolasBankDepositOrder.address).offset(offset).limit(limit).all()
        except OperationalError:
            logging.error(f"Database operation failed.")
            return False, []
        finally:
            s.close()

        infos = []
        for i in result:
            info = {
                "address": i.address,
                "product_id": i.product_id
            }

            infos.append(info)

        return True, infos

    def GetBalanceOfAccount(self, address, productId):
        s = self.session()

        try:
            result = s.query(ViolasBankDepositOrder.total_value).filter(ViolasBankDepositOrder.address == address).filter(ViolasBankDepositOrder.product_id == productId).filter(ViolasBankDepositOrder.status == 0).order_by(ViolasBankDepositOrder.id.desc()).first()
        except OperationalError:
            logging.error(f"Database operation failed.")
            return False, None
        finally:
            s.close()

        return True, result.total_value

    def GetLastInterest(self, address, productId):
        s = self.session()

        try:
            result = s.query(ViolasBankInterestInfo.total_interest).filter(ViolasBankInterestInfo.address == address).filter(ViolasBankInterestInfo.product_id == productId).order_by(ViolasBankInterestInfo.id.desc()).first()
        except OperationalError:
            logging.error(f"Database operation failed.")
            return False, None
        finally:
            s.close()

        if result:
            return True, result.total_interest
        else:
            return True, 0

    def InsertNewInterest(self, address, interest, total_interest, date, product_id):
        s = self.session()

        try:
            interestInfo = ViolasBankInterestInfo(
                address = address,
                interest = interest,
                total_interest = total_interest,
                date = date,
                product_id = product_id
            )

            s.add(interestInfo)
            s.commit()
        except OperationalError:
            logging.error(f"Database operation failed.")
            return False
        finally:
            s.close()

        return True

    def GetProductInfo(self, productId):
        s = self.session()

        try:
            result = s.query(ViolasBankDepositProduct).filter(ViolasBankDepositProduct.product_id == productId).first()
        except OperationalError:
            logging.error(f"Database operation failed.")
            return False, None
        finally:
            s.close()

        info = {
            "currency": result.currency
        }

        return True, info
