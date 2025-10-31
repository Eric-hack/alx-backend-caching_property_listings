from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

def get_all_properties():
    """
    Fetch all Property objects from Redis cache if available,
    otherwise query the database and store in cache for 1 hour.
    """
    cached_properties = cache.get("all_properties")
    if cached_properties is not None:
        return cached_properties  # Cache hit

    # Cache miss: fetch from database
    properties = list(Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    ))
    cache.set("all_properties", properties, 3600)  # Cache for 1 hour
    return properties


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    Returns:
        dict: {
            "hits": int,
            "misses": int,
            "hit_ratio": float
        }
    """
    # Get Redis connection configured as Django cache backend
    redis_conn = get_redis_connection("default")
    
    # Get Redis INFO stats
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    # Log metrics
    logger.info(f"Redis Cache Metrics — Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

    # Return structured data
    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }
