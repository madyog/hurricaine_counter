from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from hurricanes.service.hurricane_service import HurricaneService
from django.http import HttpResponse

def hurricane_view(request):
    service = HurricaneService()
    results = service.count_florida_hurricanes()
    formatted = "\n".join(results)  # each item on new line
    return HttpResponse(formatted, content_type="text/plain")
