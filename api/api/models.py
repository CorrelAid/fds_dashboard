# coding: utf-8
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    slug = Column(String(30))
    start_date = Column(TIMESTAMP(precision=6))
    active = Column(Boolean)


class Jurisdiction(Base):
    __tablename__ = 'jurisdictions'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))


class PublicBody(Base):
    __tablename__ = 'public_bodies'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    jurisdiction_id = Column(ForeignKey('jurisdictions.id'))

    jurisdiction = relationship('Jurisdiction')


class FoiRequest(Base):
    __tablename__ = 'foi_requests'

    id = Column(Integer, primary_key=True)
    jurisdiction_id = Column(ForeignKey('jurisdictions.id'))
    refusal_reason = Column(String(750))
    costs = Column(Numeric)
    due_date = Column(TIMESTAMP(precision=6))
    created_at = Column(TIMESTAMP(precision=6))
    last_message = Column(TIMESTAMP(precision=6))
    status = Column(String(26))
    resolution = Column(String(26))
    user_id = Column(Integer)
    public_body_id = Column(ForeignKey('public_bodies.id'))
    campaign_id = Column(ForeignKey('campaigns.id'))

    campaign = relationship('Campaign')
    jurisdiction = relationship('Jurisdiction')
    public_body = relationship('PublicBody')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    foi_request_id = Column(ForeignKey('foi_requests.id'))
    sent = Column(Boolean)
    is_response = Column(Boolean)
    is_postal = Column(Boolean)
    kind = Column(String(15))
    sender_public_body_id = Column(Integer)
    recipient_public_body_id = Column(Integer)
    status = Column(String(20))
    timestamp = Column(TIMESTAMP(precision=6))

    foi_request = relationship('FoiRequest')
