from django.contrib.auth.models import User
from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField(default=0)  # Optional: parse from Last.fm if available

    # New fields from Last.fm
    album_art_url = models.URLField(blank=True)
    lastfm_url = models.URLField(blank=True)
    lastfm_id = models.CharField(max_length=100, blank=True)
    mbid = models.CharField(max_length=100, blank=True)

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} – {self.title}"



class WeeklyPick(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="weekly_picks")
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    selected_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Week {self.week_start_date} - {self.week_end_date}: {self.album}"
    
class Review(models.Model):
    weekly_album = models.ForeignKey("WeeklyPick", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link review to a user
    rating = models.PositiveIntegerField()  # 0-100 rating
    text = models.TextField()
    favorite_song = models.CharField(max_length=200)
    least_favorite_song = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('weekly_album', 'user')  # Ensures one review per user per weekly album

    def __str__(self):
        return f"Review by {self.user.username} on {self.weekly_album.album.title}"

