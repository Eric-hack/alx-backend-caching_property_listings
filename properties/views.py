from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property

# Cache view response for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all()
    return render(request, "properties/property_list.html", {"properties": properties})
