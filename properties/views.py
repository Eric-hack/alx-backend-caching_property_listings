from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

# Cache the JSON response for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    )
    data = list(properties)  # Convert queryset to list
    return JsonResponse({"data": data})
