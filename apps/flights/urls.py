# apps/flights/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.fetch_flights, name="get_flights"),
]
