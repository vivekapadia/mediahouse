# src/models/movie.py
from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.association import movie_actor, movie_genre
from .actor import Actor  # Import from the same package
from .genre import Genre  # Import from the same package

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    release_date = Column(Date)
    language = Column(String(10))
    rating = Column(Float)
    popularity = Column(Float)
    vote_count = Column(Integer)
    poster_path = Column(String(255))
    backdrop_path = Column(String(255))
    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")