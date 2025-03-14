from django.urls import path
from .views import home, album_list, weekly_pick

urlpatterns = [
    path('', home, name='home'),
    path('albums/', album_list, name='album_list'),
    path('weekly-pick/', weekly_pick, name='weekly_pick'),  # Add this
]
