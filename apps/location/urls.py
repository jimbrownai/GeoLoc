# apps/location/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("details/", views.get_location_details, name="get_location_details"),
    path("fetch/", views.fetch_location, name="fetch_location"),
    path("airports/", views.nearby_airports, name="nearby_airports"),
]
