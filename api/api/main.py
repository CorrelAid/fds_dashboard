import os
import uvicorn
import sys
import databases
import sqlalchemy
from typing import Union
from fastapi import FastAPI, status, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models 
from schemas import Stats, GeneralInfo, Ranking_public_body, Ranking_jurisdiction
from database import SessionLocal,engine,metadata
from helpers import generate_model
from queries import query_general_info, query_stats, query_general_info, query_ranking_jurisdiction, query_ranking_public_body
from cache import cache_handler


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

    
@app.get("/",response_model=Stats)
def root(db: Session = Depends(get_db),
         l: Union[str, None] = Query(default=None, max_length=15),
         s: Union[int, str, None] = Query(default=None)):
    return cache_handler(db = db, l = l, s=s, key =  f"stats_{l}_{s}", query_function = query_stats)

@app.get("/general_info",response_model=GeneralInfo)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, l = None, s= None, key = "general_info", query_function = query_general_info)

@app.get("/ranking_public_body",response_model=Ranking_public_body)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, l = None, s= None, key = "ranking_public_body", query_function = query_ranking_public_body)

@app.get("/ranking_jurisdiction",response_model=Ranking_jurisdiction)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, l = None, s= None, key = "ranking_jurisdiction", query_function = query_ranking_jurisdiction)


# def start():
#     """Launched with `poetry run start` at root level"""
#     # Generating sqlalchemy model 
#     generate_model(engine=engine, metadata=metadata, outfile='kn_fds_statistics_api/models.py') 
#     uvicorn.run("kn_fds_statistics_api.main:app", host="0.0.0.0", port=8000, reload=True)