from django.contrib.auth.models import User
from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Now linked to User
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.title}"


class WeeklyPick(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="weekly_picks")
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    selected_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Week {self.week_start_date} - {self.week_end_date}: {self.album}"
