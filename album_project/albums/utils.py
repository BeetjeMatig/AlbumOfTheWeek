import random
from datetime import date, timedelta
from albums.models import Album, WeeklyPick

def select_random_weekly_picks():
    """Randomly selects albums for the current and past two weeks if no pick exists for those weeks."""
    
    today = date.today()
    weeks = [
        today - timedelta(days=today.weekday()),  # Current week start (Monday)
        today - timedelta(weeks=1, days=today.weekday()),  # Last week start
        today - timedelta(weeks=2, days=today.weekday())  # Two weeks ago start
    ]
    
    # Get all albums
    albums = list(Album.objects.all())
    if len(albums) < 3:
        print("Not enough albums in the database to select three weekly picks.")
        return
    
    # Shuffle to get random albums
    random.shuffle(albums)

    for i, week_start in enumerate(weeks):
        week_end = week_start + timedelta(days=6)

        # Check if a pick already exists for this week
        if WeeklyPick.objects.filter(week_start_date=week_start).exists():
            print(f"Weekly pick for {week_start} - {week_end} already exists.")
            continue

        # Assign a new random album for this week
        WeeklyPick.objects.create(album=albums[i], week_start_date=week_start, week_end_date=week_end)
        print(f"Selected {albums[i].artist} - {albums[i].title} for {week_start} - {week_end}.")
