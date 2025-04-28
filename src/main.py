from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.movie import Movie as MovieModel
from src.models.actor import Actor as ActorModel
from src.models.genre import Genre as GenreModel
from src.schemas import MovieCreate, ActorCreate, GenreCreate

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Movie CRUD
@app.post("/movies/", response_model=MovieCreate)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = MovieModel(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=list[MovieCreate])
def list_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(MovieModel).offset(skip).limit(limit).all()

@app.get("/movies/{movie_id}", response_model=MovieCreate)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/movies/{movie_id}", response_model=MovieCreate)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = db.get(MovieModel, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.get(MovieModel, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return {"detail": "Deleted"}

# Actor CRUD
@app.post("/actors/", response_model=ActorCreate)
def create_actor(actor: ActorCreate, db: Session = Depends(get_db)):
    db_actor = ActorModel(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@app.get("/actors/", response_model=list[ActorCreate])
def list_actors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ActorModel).offset(skip).limit(limit).all()

@app.get("/actors/{actor_id}", response_model=ActorCreate)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.get(ActorModel, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

@app.put("/actors/{actor_id}", response_model=ActorCreate)
def update_actor(actor_id: int, actor: ActorCreate, db: Session = Depends(get_db)):
    db_actor = db.get(ActorModel, actor_id)
    if not db_actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    for key, value in actor.dict().items():
        setattr(db_actor, key, value)
    db.commit()
    db.refresh(db_actor)
    return db_actor

@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    db_actor = db.get(ActorModel, actor_id)
    if not db_actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    db.delete(db_actor)
    db.commit()
    return {"detail": "Deleted"}

# Genre CRUD
@app.post("/genres/", response_model=GenreCreate)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = GenreModel(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.get("/genres/", response_model=list[GenreCreate])
def list_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(GenreModel).offset(skip).limit(limit).all()

@app.get("/genres/{genre_id}", response_model=GenreCreate)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.get(GenreModel, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@app.put("/genres/{genre_id}", response_model=GenreCreate)
def update_genre(genre_id: int, genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = db.get(GenreModel, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    for key, value in genre.dict().items():
        setattr(db_genre, key, value)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.delete("/genres/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = db.get(GenreModel, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    db.delete(db_genre)
    db.commit()
    return {"detail": "Deleted"}