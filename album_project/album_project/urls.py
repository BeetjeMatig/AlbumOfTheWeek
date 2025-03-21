from django.contrib import admin
from django.urls import path, include
from albums.views import register
from albums.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('albums.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile, name='profile'),  # ← add this
    path('accounts/register/', register, name='register'),
]

