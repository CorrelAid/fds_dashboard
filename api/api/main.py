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
from schemas import Stats, GeneralInfo, Ranking
from database import SessionLocal,engine,metadata
from queries.general_info import query_general_info
from queries.stats import query_stats
from queries.general_info import query_general_info
from queries.rankings import query_ranking
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
    return cache_handler(db = db, l = l, s = s, ascending = None, key =  f"stats_{l}_{s}", query_function = query_stats)

@app.get("/general_info",response_model=GeneralInfo)
def root(db: Session = Depends(get_db)):
    return cache_handler(db, ascending = None, l = None, s = None, key = "general_info", query_function = query_general_info)

@app.get("/ranking",response_model=Ranking)
def root(db: Session = Depends(get_db),
         typ: Union[str, None] = Query(default="public_bodies", max_length=15),
         s: Union[str, None] = Query(default='Verspaetungsquote', max_length=25),
         ascending: Union[bool, None] = Query(default = True)):
    return cache_handler(db, l = None, s = s, ascending = ascending, key = f"ranking_{typ}_{s}_{ascending}", typ=typ, query_function = query_ranking)



# def start():
#     """Launched with `poetry run start` at root level"""
#     # Generating sqlalchemy model 
#     generate_model(engine=engine, metadata=metadata, outfile='kn_fds_statistics_api/models.py') 
#     uvicorn.run("kn_fds_statistics_api.main:app", host="0.0.0.0", port=8000, reload=True)