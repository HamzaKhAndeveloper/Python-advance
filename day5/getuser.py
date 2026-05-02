from fastapi  import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError ,jwt
import os 
from dotenv import load_dotenv
load_dotenv()

oauth_2 = OAuth2PasswordBearer(tokenUrl = "login")
ALGORITHM = "HS256"
SECRET = os.getenv("SECRET")

def get_user(token: str = Depends(oauth_2)):
    try:
        playload = jwt.decode(token , SECRET,algorithms = [ALGORITHM])
        id = playload.get("user_id")
        return id
    except JWTError:
        raise HTTPException(status_code=401,detail= "invalid user")    