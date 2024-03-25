from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from typing import Annotated, List
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int


class CustomerBase(BaseModel):
    name: str
    email: str = None
    phone: str = None

    class Config:
        from_attributes = True


class Customer(CustomerBase):
    id: int


class AccountBase(BaseModel):
    account_number: str
    account_type: str
    balance: float
    customer_id: int

    class Config:
        from_attributes = True


class Account(AccountBase):
    id: int
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TransactionBase(BaseModel):
    transaction_type: str
    amount: float
    account_id: int


class Transaction(TransactionBase):
    id: int
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserBase(BaseModel):
    username: str
    password_hash: str
    customer_id: int
    class Config:
        from_attributes = True


class User(UserBase):
    id: int


class AccountWithTransactions(BaseModel):
    account: model.Account
    transactions: 'List[Transaction]'


class CustomerWithAccounts(BaseModel):
    customer: model.Customer
    accounts: 'List[AccountWithTransactions]'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


# POST FastAPI endpoints
@app.post("/customers/", status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerBase, db: Session = Depends(get_db)):
    db_customer = model.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.post("/accounts/", status_code=status.HTTP_201_CREATED)
def create_account(account: AccountBase, db: Session = Depends(get_db)):
    db_account = model.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@app.post("/transactions/", status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionBase, db: Session = Depends(get_db)):
    db_transaction = model.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = model.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# GET FastAPI endpoints
@app.get("/customers/{customer_id}", response_model=CustomerWithAccounts)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    # Fetch customer by ID
    customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Fetch accounts related to the customer
    accounts = db.query(model.Account).filter(model.Account.customer_id == customer_id).all()

    # Fetch transactions related to each account
    for account in accounts:
        account_transactions = db.query(model.Transaction).filter(model.Transaction.account_id == account.id).all()
        setattr(account, 'transactions', account_transactions)

    return CustomerWithAccounts(customer=customer, accounts=accounts)
'''
@app.get("/customers/{customer_id}", response_model=CustomerWithAccounts)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    # Fetch customer by ID
    customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Fetch accounts related to the customer
    accounts = db.query(model.Account).filter(model.Account.customer_id == customer_id).all()

    # Fetch transactions related to the customer's accounts
    for account in accounts:
        account.transactions = db.query(model.Transaction).filter(model.Transaction.account_id == account.id).all()

    # Add accounts and transactions to customer object
    customer.accounts = accounts

    return customer


async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer
'''

@app.get("/accounts/{account_id}", response_model=Account)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(model.Account).filter(model.Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(model.Transaction).filter(model.Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# select query
@app.get("/list_customers/", response_model=List[Customer])
def get_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = db.query(model.Customer).offset(skip).limit(limit).all()
    return customers


@app.get("/list_accounts/", response_model=List[Account])
def get_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    accounts = db.query(model.Account).offset(skip).limit(limit).all()
    return accounts


@app.get("/list_transactions/", response_model=List[Transaction])
def get_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(model.Transaction).offset(skip).limit(limit).all()
    return transactions


@app.get("/list_users/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(model.User).offset(skip).limit(limit).all()
    return users
