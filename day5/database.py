from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

LocalSession = sessionmaker(bind = engine,autocommit = False,autoflush = False)

Base = declarative_base()

def getdb():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()    