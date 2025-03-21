from django.urls import path
from .views import home, album_list, weekly_pick, submit_album

urlpatterns = [
    path('', home, name='home'),
    path('albums/', album_list, name='album_list'),
    path('weekly-pick/', weekly_pick, name='weekly_pick'),
    path('submit/', submit_album, name='submit_album'),
]
