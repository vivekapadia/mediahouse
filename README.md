## Project Documentation: FastAPI Movie Platform

This document captures all steps, explanations, and configurations necessary to build a Movie Platform backend using **Python 3.13.2**, **FastAPI**, **SQLAlchemy**, **Alembic**, and **PostgreSQL**. It is intended for beginners and will be continuously updated with each new step.

---

### 1. Prerequisites

- **Python 3.13.2** installed on Windows 11 (CMD terminal available).
- **PostgreSQL** installed and a database named `mediahouse` created.
- **Git repository** initialized in `D:\Learning\Pycharm\mediahouse`.
- **PyCharm** (or VS Code) available.
- **Internet access** for TMDB account creation and API usage (TMDB API is free for non-commercial use).

---

### 2. Folder Structure (Current)

```
D:\Learning\Pycharm\mediahouse\
├── .gitignore
├── .venv/         # Python virtual environment
├── .env           # Environment variables file
├── README.md      # This documentation file
└── src/           # Application source code
    ├── config.py
    ├── database.py
    ├── models/    # ORM models
    │   ├── __init__.py
    │   ├── movie.py
    │   ├── actor.py
    │   ├── genre.py
    │   └── association.py
    ├── schemas.py # Pydantic schemas
    ├── main.py    # FastAPI entrypoint
    └── ingest.py  # TMDB data ingestion script
```

*Note: You will be prompted to update `.gitignore`, `.env`, or other config files as new components are added.*

---

### 3. Initial Setup Steps (1–21)

Below are the first **21** exact steps—each with full commands (including paths), purpose, and expected outcome. Future “Next Steps” will append under this section in order.

#### Step 1: Navigate to Project Root

**Prerequisite**: Open CMD.  
**Command**:
```bat
cd D:\Learning\Pycharm\mediahouse
```
**Purpose**: Ensure correct working directory.  
**Outcome**: Prompt shows `D:\Learning\Pycharm\mediahouse>`.

#### Step 2: Create Virtual Environment

**Prerequisite**: Python on PATH.  
**Command**:
```bat
python -m venv D:\Learning\Pycharm\mediahouse\.venv
```
**Purpose**: Isolate dependencies.  
**Outcome**: `.venv` folder created.

#### Step 3: Update `.gitignore`

**Action**: Add to `.gitignore`:
```text
# Virtual environment
.venv/

# Environment variables
.env

# Python compiled files
__pycache__/
*.pyc

# IDE folders
.idea/
.vscode/
```
**Purpose**: Prevent committing sensitive/generated files.  
**Outcome**: `.gitignore` updated.

#### Step 4: Activate Virtual Environment

**Command**:
```bat
D:\Learning\Pycharm\mediahouse\.venv\Scripts\activate
```
**Purpose**: Use isolated environment.  
**Outcome**: Prompt prefixed with `(venv)`.

#### Step 5: Install Core Dependencies

**Command**:
```bat
pip install "fastapi[standard]" uvicorn[standard] SQLAlchemy alembic psycopg2-binary python-dotenv requests
```
**Purpose**: Install FastAPI, server, ORM, migrations, DB driver, dotenv, HTTP client.  
**Outcome**: Packages available (`pip list`).

#### Step 6: Scaffold Project Structure

```bat
mkdir src && mkdir src\models
```  
```bat
type nul > src\config.py
 type nul > src\database.py
 type nul > src\schemas.py
 type nul > src\models\__init__.py
 type nul > src\main.py
 type nul > src\ingest.py
```  
**Purpose**: Prepare code and placeholders.  
**Outcome**: Files created.

#### Step 7: Register for TMDB API Key

1. Visit https://www.themoviedb.org/signup and register.
2. Verify your email.
3. Go to Settings → API, request a **Developer** key, copy the **v3 API Key**.
**Purpose**: Obtain free TMDB API key.  
**Outcome**: API key ready.

#### Step 8: Create and Configure `.env`

```bat
type nul > .env
```  
Add:
```env
DATABASE_URL=postgresql+psycopg2://<db_user>:<db_pass>@localhost/mediahouse
TMDB_API_KEY=<your_tmdb_api_key>
```
**Purpose**: Store sensitive settings.  
**Outcome**: `.env` populated.

#### Step 9: Load Environment Variables

**File**: `src/config.py`
```python
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
```
**Purpose**: Centralize config.  
**Outcome**: Variables available.

#### Step 10: Setup Database Connection

**File**: `src/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
```
**Purpose**: Engine, session, base.  
**Outcome**: DB connection ready.

#### Step 11: Initialize Alembic

```bat
alembic init migrations
```  
**Purpose**: Scaffold migrations.  
**Outcome**: `migrations/` and `alembic.ini`.

#### Step 12: Configure Alembic

- In `alembic.ini`: `sqlalchemy.url = ${DATABASE_URL}`
- In `migrations/env.py`, at top:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  from src.database import Base
  from src.models import association, movie, actor, genre

  target_metadata = Base.metadata
  ```
**Purpose**: Link models and env.  
**Outcome**: Autogenerate works.

#### Step 13: Define Association Tables

**File**: `src/models/association.py`
```python
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
```
**Purpose**: Many-to-many support.  
**Outcome**: Association tables defined.

#### Step 14: Define Models

**File**: `src/models/movie.py`
```python
from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.association import movie_actor, movie_genre

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
```

**File**: `src/models/actor.py`
```python
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.association import movie_actor

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    gender = Column(String(10))
    profile_path = Column(String(255))
    birthdate = Column(Date)
    biography = Column(String(500))
    place_of_birth = Column(String(255))
    popularity = Column(Float)
    known_for_department = Column(String(100))
    death_date = Column(Date)
    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")
```

**File**: `src/models/genre.py`
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.association import movie_genre

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    type = Column(String(50))
    origin = Column(String(50))
    created_by = Column(String(100))
    updated_by = Column(String(100))
    created_at = Column(String(20))
    updated_at = Column(String(20))
    is_active = Column(Boolean, default=True)
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")
```

#### Step 15: Generate Initial Migration

```bat
alembic revision --autogenerate -m "Initial migration"
```  
**Purpose**: Create migration script.  
**Outcome**: File under `migrations/versions/`.

#### Step 16: Apply Migrations

```bat
alembic upgrade head
```  
**Purpose**: Execute migrations.  
**Outcome**: Tables created.

#### Step 17: Verify Schema

```bat
psql -d mediahouse -U postgres -c "\dt"
```  
**Purpose**: Confirm table creation.  
**Outcome**: Five tables listed.

#### Step 18: Scaffold CRUD Routers

**File**: `src/schemas.py`
```python
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
```

**File**: `src/main.py`
```python
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
```

#### Step 19: Run & Test with Swagger UI

```bat
uvicorn src.main:app --reload
```

**Purpose**: Launch development server with interactive docs at `/docs`.

**Outcome**: Manually test all CRUD endpoints.

#### Step 20: Ingest TMDB Data

**File**: `src/ingest.py`
```python
import requests
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.movie import Movie as MovieModel
from src.config import TMDB_API_KEY
from datetime import datetime

session: Session = SessionLocal()
for page in range(1, 51):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
    response = requests.get(url)
    response.raise_for_status()
    for item in response.json().get('results', []):
        release = None
        try:
            release = datetime.strptime(item.get('release_date',''), '%Y-%m-%d').date()
        except:
            pass
        movie = MovieModel(
            title=item.get('title'),
            description=item.get('overview'),
            release_date=release,
            language=item.get('original_language'),
            rating=item.get('vote_average'),
            popularity=item.get('popularity'),
            vote_count=item.get('vote_count'),
            poster_path=item.get('poster_path'),
            backdrop_path=item.get('backdrop_path'),
        )
        session.add(movie)
session.commit()
session.close()
```

**Explanation**: This script fetches paginated movie data from TMDB’s “popular” endpoint, parses dates, and bulk inserts into your `movies` table via SQLAlchemy.

**Outcome**: The `movies` table populates with 1000+ records.

#### Step 21: Commit Initial Feature Set

```bat
git add .
git commit -m "Initial backend setup: models, migrations, CRUD, TMDB ingestion"
```

**Purpose**: Record the current stable state in version control.

**Outcome**: Your Git repository now contains the initial backend feature set.
#### Step 22: Install Authentication Dependencies

**Prerequisite**: Virtual environment active.\
**Command**:

```bat
.venv\Scripts\activate
pip install python-jose[cryptography] passlib[bcrypt]
```

**Purpose**: Add JWT support (`python-jose`) and password hashing (`passlib[bcrypt]`).\
**Outcome**: Dependencies available (`pip list`).

#### Step 23: Define User Model & Migration

**File**: `src/models/user.py` (create via CMD):

```bat
 type nul > src/models/user.py
```

**Code**:

```python
from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
```

**Commands**:

```bat
alembic revision --autogenerate -m "add users table"
alembic upgrade head
```

**Purpose**: Create `users` table.\
**Outcome**: Table exists in PostgreSQL.

#### Step 24: Add Authentication Schemas

**File**: `src/schemas.py` (append):

```python
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

**Purpose**: Validate user signup/login data.\
**Outcome**: Pydantic models ready.

#### Step 25: Implement Signup Endpoint

**File**: `src/main.py` (append):

```python
from passlib.context import CryptContext
from src.models.user import User as UserModel
from src.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/users/signup", response_model=UserCreate)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = pwd_context.hash(user.password)
    db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user
```

**Purpose**: Register new users with hashed passwords.\
**Outcome**: `users` table populated.

#### Step 26: Implement Login & JWT Issuance

**File**: `src/main.py` (append):

```python
from jose import jwt
from datetime import datetime, timedelta
from src.schemas import Token

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/users/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter_by(username=user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": db_user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
```

**Purpose**: Authenticate users and issue JWTs.\
**Outcome**: Returns access tokens.

#### Step 27: Secure Routes with JWT

**File**: `src/main.py` (append):

```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(401, "Invalid token")
        return username
    except JWTError:
        raise HTTPException(401, "Invalid token")

@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"user": current_user}
```

**Purpose**: Enforce authentication on endpoints.\
**Outcome**: Unauthorized access returns 401.

#### Step 28: Create Dockerfile

```bat
type nul > Dockerfile
```

**File**: `Dockerfile`

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn","src.main:app","--host","0.0.0.0","--port","80"]
```

**Purpose**: Containerize the application.\
**Outcome**: Dockerfile ready.

#### Step 29: Create docker-compose.yml

```bat
type nul > docker-compose.yml
```

**File**: `docker-compose.yml`

```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:80"
    env_file:
      - .env
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mediahouse
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

**Purpose**: Define multi-container setup.\
**Outcome**: Compose file configured.

#### Step 30: Deploy with Docker Compose

```bat
docker-compose up -d
```

**Purpose**: Launch web and DB containers.\
**Outcome**: App accessible at `http://localhost:8000/docs`.

#### Step 31: Clean Up & Commit

```bat
docker-compose down
git add Dockerfile docker-compose.yml
git commit -m "Add Docker support"
```

**Purpose**: Stop containers and commit changes.\
**Outcome**: Docker support recorded in Git.

---

> **Note**: All code and steps remain in strict sequence to avoid errors. Any future additions will append under Section 3 without altering existing numbering or order.

