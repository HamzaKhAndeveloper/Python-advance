from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from load_dotenv import load_dotenv
load_dotenv()
import os
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()