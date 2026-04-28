from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependies import getdb
from sqlalchemy.orm import Session
from models.usertable import User


router = APIRouter()

class User1(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str
@router.post("/signup")
def create_user(user: User1 , db: Session = Depends(getdb)):
    user1 = db.query(User).filter(User.email == user.email).first()
    if user1 is not None:
        return {"message":"user already exists"}
    user1 = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(user1)
    db.commit()
    return {"message":"user created successfully"}
    
@router.post("/login")
def login_user(user: Login , db: Session = Depends(getdb)):
    user1 = db.query(User).filter(User.email == user.email).first()
    if user1 is None:
        return {"message":"user not found"}
    if user1.password == user.password:
        return {"message":"user logged in successfully"}
    return {"message":"invalid credentials"}

@router.get("/user/{id}")
def get_user(id: int , db: Session = Depends(getdb)):
    user1 = db.query(User).filter(User.id == id).first()
    if user1 is None:
        return {"message":"user not found"}
    return user1    