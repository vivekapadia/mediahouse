from sqlalchemy import Table, Column, ForeignKey
from src.database import Base

movie_actor = Table(
    'movie_actor', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
)

movie_genre = Table(
    'movie_genre', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True),
)