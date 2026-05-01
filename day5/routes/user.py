from fastapi import APIRouter,Depends , HTTPException
from models.user_model import User
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import getdb

class UserSchema(BaseModel):
    name: str 
    age: int 

router = APIRouter()

@router.post("/user",status_code = 201)
def createuser(user: UserSchema,db: Session = Depends(getdb)):
    try:
        newuser = User(
            name = user.name,
            age = user.age
        )
        db.add(newuser)
        db.commit()
        return {"message": "create successfully"}
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code = 500 , detail = f"server error: {str(e)}",)   

