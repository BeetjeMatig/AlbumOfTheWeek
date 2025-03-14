from django.core.management.base import BaseCommand
from albums.utils import select_random_weekly_picks

class Command(BaseCommand):
    help = "Randomly selects weekly albums if they haven't been picked yet."

    def handle(self, *args, **kwargs):
        select_random_weekly_picks()
        self.stdout.write(self.style.SUCCESS("Weekly album selection process completed."))
