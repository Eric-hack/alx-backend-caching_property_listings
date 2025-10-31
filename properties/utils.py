from django.core.cache import cache
from .models import Property

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
