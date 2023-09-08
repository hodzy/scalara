from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_files, name='search'),
    path('/download/<slug:file_key>', views.download_files, name='download'),
]