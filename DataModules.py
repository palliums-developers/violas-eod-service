from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, SmallInteger, Integer, BigInteger, String, Numeric, Text

Base = declarative_base()

class ViolasBankDepositProduct(Base):
    __tablename__ = "deposit_product"

    id = Column(BigInteger, primary_key = True, autoincrement = True)
    product_id = Column(String(32), primary_key = True, nullable = False)
    product_name = Column(String(32), nullable = False)
    logo = Column(String(32), nullable = False)
    minimum_amount = Column(Integer, nullable = False)
    minimum_step = Column(Integer, nullable = False)
    max_limit = Column(Integer, nullable = False)
    pledge_rate = Column(Numeric, nullable = False)
    description = Column(Text, nullable = False)
    intor = Column(Text, nullable = False)
    question = Column(Text, nullable = False)
    currency = Column(String(16), nullable = False)
    rate = Column(Numeric, nullable = True)
    rate_desc = Column(Text, nullable = True)

class ViolasBankDepositOrder(Base):
    __tablename__ = "deposit_order"

    id = Column(BigInteger, primary_key = True, autoincrement = True)
    order_id = Column(String(32), primary_key = True, nullable = False)
    product_id = Column(String(32), nullable = False)
    address = Column(String(64), nullable = False)
    value = Column(BigInteger, nullable = False)
    total_value = Column(BigInteger, nullable = False)
    date = Column(Integer, nullable = False)
    order_type  = Column(SmallInteger, nullable = False) # 0: deposit, 1: withdrawal
    status = Column(SmallInteger, nullable = False) # 0: succ, -1: failed

class ViolasBankInterestInfo(Base):
    __tablename__ = "interest_info"

    id = Column(BigInteger, primary_key = True, autoincrement = True)
    address = Column(String(64), nullable = False)
    interest = Column(BigInteger, nullable = False)
    total_interest = Column(BigInteger, nullable = False)
    date = Column(Integer, nullable = False)
    product_id = Column(String(32), nullable = False)
