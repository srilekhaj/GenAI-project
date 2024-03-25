from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int


class UserBase(BaseModel):
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code= status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = model.User(**user.dict())
    #we can get all data from user deserialize into obj
    db.add(user)
    db.commit()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}