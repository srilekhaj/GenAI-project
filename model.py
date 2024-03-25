from sqlalchemy import Column, Integer, String, REAL, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from database import Base

'''class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    account_number = Column(String(50), unique=True, index=True)
    balance = Column(Float, default=0)
'''


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(50))
    user_id = Column(Integer)


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50))
    phone = Column(String(50))
    accounts = relationship("Account", back_populates="customer")
    users = relationship("User", back_populates="customer")



class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_number = Column(String(50), unique=True)
    account_type = Column(String(50))
    balance = Column(REAL, default=0)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_type = Column(String(50))
    amount = Column(REAL)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    # timestamp = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    account_id = Column(Integer, ForeignKey('account.id'))
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship("Account", back_populates="transactions")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(50))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="users")