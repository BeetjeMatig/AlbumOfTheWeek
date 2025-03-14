import pandas as pd
from django.core.management.base import BaseCommand
from albums.models import Album
import numpy as np

class Command(BaseCommand):
    help = "Import albums from an Excel file with headers: 'Your name', 'Artist', 'Album title', 'Genre', 'Release year'"

    def add_arguments(self, parser):
        parser.add_argument("excel_file", type=str, help="Path to the Excel file")

    def handle(self, *args, **kwargs):
        excel_file = kwargs["excel_file"]
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            self.stderr.write(f"Error reading the Excel file: {e}")
            return

        # Ensure expected columns exist
        expected_columns = ['Your name', 'Artist', 'Album title', 'Genre', 'Release year']
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            self.stderr.write(f"Missing expected columns: {', '.join(missing_columns)}")
            return

        for index, row in df.iterrows():
            submitted_by = row.get("Your name")
            artist = row.get("Artist")
            title = row.get("Album title")
            genre = row.get("Genre")
            release_year = row.get("Release year")

            # Validate required fields: Artist and Album title
            if pd.isnull(artist) or pd.isnull(title):
                self.stderr.write(f"Skipping row {index}: Missing required 'Artist' or 'Album title'.")
                continue

            # Convert release_year to an integer if it's not null
            try:
                if np.isnan(release_year):
                    release_year_int = None
                else:
                    release_year_int = int(release_year)
            except Exception:
                self.stderr.write(f"Invalid release year at row {index}: {release_year}. Skipping row.")
                continue

            album, created = Album.objects.get_or_create(
                title=title,
                artist=artist,
                defaults={
                    "submitted_by": submitted_by,
                    "genre": genre,
                    "release_year": release_year_int
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added album: {album}"))
            else:
                self.stdout.write(f"Album already exists: {album}")

        self.stdout.write(self.style.SUCCESS("Import complete."))
