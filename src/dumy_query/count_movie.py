from src.database import SessionLocal
from src.models.movie import Movie

def main():
    db = SessionLocal()
    print("Total movies:", db.query(Movie).count())
    db.close()

if __name__ == "__main__":
    main()
