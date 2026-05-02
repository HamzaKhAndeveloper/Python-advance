from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"

pwd = CryptContext(schemes = ["bcrypt"],deprecated = "auto")

def hashpassword(password: str):
    return pwd.hash(password)

def verify(plain,hashpass):
    return pwd.verify(plain,hashpass)    

def createjwt(data: dict):
    jwtload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    jwtload.update({"exp":expire})
    return jwt.encode(jwtload,SECRET_KEY,ALGORITHM)

