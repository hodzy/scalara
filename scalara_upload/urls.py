from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_files, name='upload'),
    path('upload', views.upload_files, name='upload'),
]