# coding: utf-8
from sqlalchemy import Boolean, Column, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FoiRequest(Base):
    __tablename__ = 'foi_requests'

    id = Column(Integer, primary_key=True)
    jurisdiction = Column(String(100))
    refusal_reason = Column(String(750))
    costs = Column(Numeric)
    due_date = Column(TIMESTAMP(precision=6))
    resolved_on = Column(TIMESTAMP(precision=6))
    first_message = Column(TIMESTAMP(precision=6))
    last_message = Column(TIMESTAMP(precision=6))
    status = Column(String(26))
    resolution = Column(String(26))
    user_id = Column(Numeric)
    public_body_id = Column(Numeric)


class Jurisdiction(Base):
    __tablename__ = 'jurisdictions'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    rank = Column(Integer)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    request = Column(Integer)
    sent = Column(Boolean)
    is_response = Column(Boolean)
    is_postal = Column(Boolean)
    kind = Column(String(15))
    sender_public_body = Column(Numeric)
    recipient_public_body = Column(Numeric)
    status = Column(String(20))
    timestamp = Column(TIMESTAMP(precision=6))


class PublicBody(Base):
    __tablename__ = 'public_bodies'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    classification = Column(Integer)
    categories = Column(Integer)
    address = Column(String(500))
    jurisdiction = Column(Integer)

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    slug = Column(String(30))
    start_date = Column(TIMESTAMP(precision=6))
    active = Column(Boolean)
