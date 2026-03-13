from sqlalchemy.orm import Session
from sqlalchemy import text
import json

try:
    from core.redis_client import redis_client
except:
    redis_client = None


def get_nearby_complaints(db: Session, lat: float, lng: float):

    cache_key = f"geo:{round(lat,3)}:{round(lng,3)}"

    # Try reading cache
    if redis_client:
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except:
            pass

    query = text("""
        SELECT
            c.complaint_id,
            c.issue_type,
            c.status,
            l.latitude,
            l.longitude,
            l.address
        FROM complaints c
        JOIN locations l
        ON c.location_id = l.location_id
        LIMIT 50
    """)

    result = db.execute(query)

    complaints = [dict(row._mapping) for row in result]

    # Try writing cache
    if redis_client:
        try:
            redis_client.setex(cache_key, 300, json.dumps(complaints))
        except:
            pass

    return complaints