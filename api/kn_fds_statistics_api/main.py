import os
import uvicorn
import sys
import databases
import sqlalchemy
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import kn_fds_statistics_api.models 
from kn_fds_statistics_api.schemas import TotalStats, GeneralInfo, Ranking
from kn_fds_statistics_api.database import SessionLocal,engine,metadata
from kn_fds_statistics_api.helpers import generate_model
from kn_fds_statistics_api.queries import query_general_info, query_total_stats, query_general_info, query_ranking
from kn_fds_statistics_api.cache import cache_handler


app = FastAPI(title="FDS Statistics API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.get("/",response_model=TotalStats)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, "total_stats", query_total_stats)

@app.get("/general_info",response_model=GeneralInfo)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, "general_info", query_general_info)

@app.get("/ranking",response_model=Ranking)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, "ranking", query_ranking)


def start():
    """Launched with `poetry run start` at root level"""
    # Generating sqlalchemy model 
    generate_model(engine=engine, metadata=metadata, outfile='kn_fds_statistics_api/models.py') 
    uvicorn.run("kn_fds_statistics_api.main:app", host="0.0.0.0", port=8000, reload=True)