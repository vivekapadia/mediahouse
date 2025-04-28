import requests
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Movie as MovieModel  # Import from src.models
from src.config import TMDB_API_KEY
from datetime import datetime
from sqlalchemy import exists

session: Session = SessionLocal()
for page in range(1, 51):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        for item in response.json().get('results', []):
            tmdb_id = item.get('id')
            if tmdb_id and session.query(exists().where(MovieModel.id == tmdb_id)).scalar():
                print(f"Movie with TMDB ID {tmdb_id} already exists. Skipping.")
                continue

            release = None
            try:
                release = datetime.strptime(item.get('release_date', ''), '%Y-%m-%d').date()
            except ValueError:
                print(f"Could not parse release date: {item.get('release_date')}")

            print(f"Fetching page {page}")
            print(f"Adding movie: {item.get('title')} (TMDB ID: {tmdb_id})")
            try:
                movie = MovieModel(
                    id=tmdb_id,
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
            except Exception as e:
                print(f"Error adding movie {item.get('title')}: {e}")
                session.rollback()

        session.commit()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()

session.close()
print("Movie ingestion complete.")