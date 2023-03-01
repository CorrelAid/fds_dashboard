from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os



POSTGRES_URL = os.environ.get("POSTGRES_URL")

engine = create_engine(POSTGRES_URL)

    

metadata = MetaData(bind=engine)
metadata.reflect()

#Each instance of SessionLocal class will be  database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

