from django.contrib import admin
from .models import Album, WeeklyPick, Review

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genre', 'release_year', 'submitted_by', 'added_on')
    search_fields = ('title', 'artist', 'genre')
    list_filter = ('genre', 'release_year')

@admin.register(WeeklyPick)
class WeeklyPickAdmin(admin.ModelAdmin):
    list_display = ('album', 'week_start_date', 'week_end_date')
    list_filter = ('week_start_date', 'week_end_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('weekly_album', 'user', 'rating', 'favorite_song', 'least_favorite_song', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'weekly_album__album__title')
