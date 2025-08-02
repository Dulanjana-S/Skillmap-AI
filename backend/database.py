from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # or your actual DB URI
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

load_dotenv()

DATABASE_USER="postgres"
DATABASE_PASSWORD="1234"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"
DATABASE_NAME="skillmap_ai"


#this is SUPABASE Connection
DATABASE_URL = os.getenv("postgresql://postgres:[Sasmitha@123]@db.mfesiyznyigpchtnsjjw.supabase.co:5432/postgres")


# PSQL Connection 
# DATABASE_URL = f"postgresql://{"postgres"}:{"1234"}@{"localhost"}:{"5432"}/{"skillmap_ai"}"


#DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
