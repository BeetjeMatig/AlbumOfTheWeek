from django.urls import path
from .views import album_list

urlpatterns = [
    path('', album_list, name='album_list'),
]
