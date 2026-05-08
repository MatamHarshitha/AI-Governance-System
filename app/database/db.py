from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

db_connect=os.getenv("database_url")
engine=create_engine(db_connect)
session_part=sessionmaker(bind=engine, autocommit=False,autoflush=False)
Base = declarative_base()