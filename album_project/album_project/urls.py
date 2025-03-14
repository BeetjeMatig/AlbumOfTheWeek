from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('albums.urls')),  # This will route the root URL to your album_list view
]
