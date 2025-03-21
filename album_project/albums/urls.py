from django.urls import path

from .views import (album_detail, album_list, fetch_album_info, home,
                    previous_picks, save_album_from_lastfm, submit_album,
                    view_reviews, weekly_pick, write_review)

urlpatterns = [
    path('', home, name='home'),
    path('albums/', album_list, name='album_list'),
    path('weekly-pick/', weekly_pick, name='weekly_pick'),
    path('weekly-pick/review/', write_review, name='write_review'),
    path('weekly-pick/reviews/', view_reviews, name='view_reviews'),
    path('weekly-pick/history/', previous_picks, name='previous_picks'),
    path('submit/', submit_album, name='submit_album'),
    path("fetch-album-info/", fetch_album_info, name="fetch_album_info"),
    path("save-album-from-lastfm/", save_album_from_lastfm, name="save_album_from_lastfm"),
    path("album/<int:pk>/", album_detail, name="album_detail"),

]
