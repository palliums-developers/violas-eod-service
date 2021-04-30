from violas_client import bank_client
from violas_client.lbrtypes.account_config.constants.lbr import CORE_CODE_ADDRESS

def MakeBankClient():
    # return bank_client.Client()
    cli = bank_client.Client.new(url="http://13.68.141.242:50001", chain_id=2)
    cli.set_bank_module_address(CORE_CODE_ADDRESS)
    cli.set_bank_owner_address("00000000000000000000000042414E4B")
    return cli
