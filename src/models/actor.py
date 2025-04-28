# src/models/actor.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.association import movie_actor

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    gender = Column(String(10))
    profile_path = Column(String(255))
    birthdate = Column(String(20))
    biography = Column(String(500))
    place_of_birth = Column(String(255))
    popularity = Column(Float)
    known_for_department = Column(String(100))
    death_date = Column(String(20))
    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")