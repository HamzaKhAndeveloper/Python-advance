from fastapi import APIRouter,Depends , HTTPException
from models.user_model import User
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import getdb
from secure import hashpassword,createjwt,verify

class UserSchema(BaseModel):
    name: str
    email: str 
    password: str 

class Login(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/user",status_code = 201)
def createuser(user: UserSchema,db: Session = Depends(getdb)):
    try:
        hashpass = hashpassword(user.password)
        newuser = User(
            name = user.name,
            email = user.email,
            password = hashpass
        )
        db.add(newuser)
        db.commit()
        return {"message": "create successfully"}
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code = 500 , detail = f"server error: {str(e)}",)   


@router.post("/login",status_code=200)
def login(user: Login,db: Session = Depends(getdb)):
    usr = db.query(User).filter(User.email == user.email).first()
    if usr is None:
        raise HTTPException(status_code=404,detail="user not found")
    if not verify(user.password,usr.password):
        raise HTTPException(status_code= 401,detail="invalid credentials") 

    token = createjwt({"sub": user.email,"user_id":usr.id}) 
    return ({"token": token,"token_type": "bearer"})   
