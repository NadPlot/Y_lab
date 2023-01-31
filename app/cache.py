import redis


# Dependency (start redis)
def get_redis():
    cache = redis.Redis(
        host='redis', port=6379, db=0,
        single_connection_client=True,
    )
    try:
        yield cache
    finally:
        cache.quit()
