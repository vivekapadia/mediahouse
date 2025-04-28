from pydantic import BaseModel
from datetime import date

class MovieCreate(BaseModel):
    title: str
    description: str | None = None
    release_date: date | None = None
    language: str | None = None
    rating: float | None = None
    popularity: float | None = None
    vote_count: int | None = None
    poster_path: str | None = None
    backdrop_path: str | None = None

class ActorCreate(BaseModel):
    name: str
    gender: str | None = None
    profile_path: str | None = None
    birthdate: date | None = None
    biography: str | None = None
    place_of_birth: str | None = None
    popularity: float | None = None
    known_for_department: str | None = None
    death_date: date | None = None

class GenreCreate(BaseModel):
    name: str
    description: str | None = None
    type: str | None = None
    origin: str | None = None
    is_active: bool | None = None