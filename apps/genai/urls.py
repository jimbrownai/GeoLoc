from django.urls import path 
from .views import travel_guide_view 

urlpatterns = [
    path("guide/", travel_guide_view, name="travel_guide"),
]