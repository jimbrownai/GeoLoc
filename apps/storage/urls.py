# apps/storage/urls.py
from django.urls import path
from . import views  # make sure views.py exists

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('download/', views.download_dataset, name='download_dataset'),
]
