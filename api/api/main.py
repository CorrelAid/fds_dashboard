from typing import Union
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api.schemas import Stats, GeneralInfo, Ranking, CampaignStarts, Reaction
from api.database import SessionLocal
from api.queries.general_info import query_general_info
from api.queries.stats import query_stats
from api.queries.rankings import query_ranking
from api.queries.campaign_starts import query_campaign_starts
from api.queries.reaction import query_reaction_time
from api.cache import cache_handler


app = FastAPI(title="FDS Statistics API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=Stats)
def root(
    db: Session = Depends(get_db),
    level: Union[str, None] = Query(default=None, max_length=15),
    selection: Union[int, None] = Query(default=None),
):
    return cache_handler(
        db=db,
        level=level,
        selection=selection,
        ascending=None,
        key=f"stats_{level}_{selection}",
        query_function=query_stats,
    )


@app.get("/general_info", response_model=GeneralInfo)
def get_general_info(db: Session = Depends(get_db)):
    return cache_handler(db, ascending=None, s=None, key="general_info", query_function=query_general_info)


@app.get("/ranking", response_model=Ranking)
def get_ranking(
    db: Session = Depends(get_db),
    typ: Union[str, None] = Query(default="public_bodies", max_length=15),
    s: Union[str, None] = Query(default="Verspaetungsquote", max_length=25),
    ascending: Union[bool, None] = Query(default=True),
):
    return cache_handler(
        db,
        s=s,
        ascending=ascending,
        key=f"ranking_{typ}_{s}_{ascending}",
        typ=typ,
        query_function=query_ranking,
    )


@app.get("/campaign_starts", response_model=CampaignStarts)
def get_campaign_starts(
    db: Session = Depends(get_db),
    typ: Union[str, None] = Query(default=None, max_length=15),
    s: Union[int, None] = Query(default=None),
):
    return cache_handler(db, typ=typ, s=s, key="campaign_starts", query_function=query_campaign_starts)


@app.get("/reaction_time", response_model=Reaction)
def get_reaction_time(
    db: Session = Depends(get_db),
    typ: Union[str, None] = Query(default=None, max_length=15),
    s: Union[int, None] = Query(default=None),
):
    return cache_handler(
        db=db, typ=typ, s=s, ascending=None, key=f"stats_{typ}_{s}", query_function=query_reaction_time
    )


# def start():
#     """Launched with `poetry run start` at root level"""
#     # Generating sqlalchemy model
#     generate_model(engine=engine, metadata=metadata, outfile='kn_fds_statistics_api/models.py')
#     uvicorn.run("kn_fds_statistics_api.main:app", host="0.0.0.0", port=8000, reload=True)
