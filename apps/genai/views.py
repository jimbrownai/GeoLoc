from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services.travel_guide import generate_travel_guide
# Create your views here.

@csrf_exempt
def travel_guide_view(request):
    if request.method == "POST" :
        try:
            data = json.loads(request.body)
            place_name = data.get("place")
            if not place_name:
                return JsonResponse({"error": "Missing 'place' in request"}, status=400)

            result = generate_travel_guide(place_name)
            return JsonResponse(result, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)