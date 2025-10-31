from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

# Still use view-level caching for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})
