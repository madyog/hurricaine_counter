from django.shortcuts import render
from hurricanes.service.hurricane_service import HurricaneService

def hurricane_view(request):
    results = None
    if request.method == "POST":  # button pressed
        service = HurricaneService()
        results = service.count_florida_hurricanes()

    return render(request, "hurricanes/hurricane_view.html", {"results": results})
