from django.urls import path
from .views import home, album_list, weekly_pick, submit_album, view_reviews, write_review

urlpatterns = [
    path('', home, name='home'),
    path('albums/', album_list, name='album_list'),
    path('weekly-pick/', weekly_pick, name='weekly_pick'),
    path('weekly-pick/review/', write_review, name='write_review'),
    path('weekly-pick/reviews/', view_reviews, name='view_reviews'),
    path('submit/', submit_album, name='submit_album'),
]
