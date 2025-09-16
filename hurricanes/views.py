from django.shortcuts import render
from hurricanes.service.hurricane_service import HurricaneService

def hurricane_view(request):
    results = None
    if request.method == "POST":
        action = request.POST.get("action")
        service = HurricaneService()

        if action == "boundary_box":
            results = service.count_florida_hurricanes(True)
        else:
            results = service.count_florida_hurricanes(False)
    return render(request, "hurricanes/hurricane_view.html", {"results": results})
