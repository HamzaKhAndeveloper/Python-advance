from fastapi import APIRouter,Depends,HTTPException
from database import getdb
from sqlalchemy.orm import Session
from models.user import User
from pydantic import BaseModel

router = APIRouter()

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    

@router.post("/user",status_code=201)
def create_user(user: UserSchema,db:Session = Depends(getdb)):
    try:
        users = User(
            username = user.username,
            email = user.email,
            password = user.password
        )
        db.add(users)
        db.commit()
        return {"message":"user created successfully"}
    except Exception:
        db.rollback()
        return HTTPException(status_code=500,detail="internal server error")

@router.get("/user",status_code=200)
def get_user(db:Session = Depends(getdb)):
    users = db.query(User).all()
    return users

@router.get("/user/{id}",status_code=200)
def get_user(id: int,db:Session = Depends(getdb)):
    users = db.query(User).filter(User.id == id).first()
    if users is None:
        raise HTTPException(status_code=404,detail="user not found")
    return users

