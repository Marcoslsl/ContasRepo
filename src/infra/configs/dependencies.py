from .database import SessionLocal


def get_db():
    """get_db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
