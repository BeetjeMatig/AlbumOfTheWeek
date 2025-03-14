from django.db import models

# Create your models here

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)  # Optional field for album cover images
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
