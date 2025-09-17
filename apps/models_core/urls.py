# apps/models_core/urls.py
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("predict/", views.predict_location, name="predict_location"),
    path("train/", views.train_model, name="train_model"),
    path("predict_place/", views.predict_place, name="predict_place"),
    path("pipeline/",csrf_exempt(views.famous_place_pipeline),name="pipeline_famous"),
    path("train/famous_places/",csrf_exempt(views.train_famous_places),name="train_famous_places")
]
