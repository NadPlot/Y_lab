import redis
from app.database import SessionLocal


# Dependency (database session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency (start redis)
def get_redis():
    cache = redis.Redis(host='redis', port=6379)
    return cache
