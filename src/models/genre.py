# src/models/genre.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.association import movie_genre

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    type = Column(String(50))
    origin = Column(String(50))
    created_by = Column(String(100))
    updated_by = Column(String(100))
    created_at = Column(String(20))
    updated_at = Column(String(20))
    is_active = Column(String(5))
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")