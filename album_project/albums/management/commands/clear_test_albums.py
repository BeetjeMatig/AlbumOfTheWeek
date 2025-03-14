from django.core.management.base import BaseCommand
from albums.models import Album, WeeklyPick

class Command(BaseCommand):
    help = "Clears all test albums and weekly picks from the database."

    def handle(self, *args, **kwargs):
        confirm = input("Are you sure you want to delete all test albums and weekly picks? (yes/no): ")
        if confirm.lower() != "yes":
            self.stdout.write(self.style.WARNING("Operation cancelled."))
            return
        
        # Delete all WeeklyPick records first (to avoid constraint issues)
        weekly_picks_deleted, _ = WeeklyPick.objects.all().delete()
        
        # Delete all albums
        albums_deleted, _ = Album.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {weekly_picks_deleted} weekly picks and {albums_deleted} albums."))
