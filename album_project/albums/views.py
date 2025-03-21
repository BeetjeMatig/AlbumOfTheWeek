from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Album
from datetime import date, timedelta
from .models import WeeklyPick
from .forms import AlbumForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    """Home page displaying the current week's album pick."""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Get Monday of the current week
    week_end = week_start + timedelta(days=6)  # Sunday of the current week

    weekly_pick = WeeklyPick.objects.filter(week_start_date=week_start).first()

    return render(request, "albums/home.html", {"weekly_pick": weekly_pick})

def weekly_pick(request):
    """Displays the current album of the week and previous selections."""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Get Monday of the current week

    # Get the current week's pick
    current_pick = WeeklyPick.objects.filter(week_start_date=week_start).first()

    # Get previous weekly picks
    past_picks = WeeklyPick.objects.exclude(week_start_date=week_start).order_by('-week_start_date')

    return render(request, "albums/weekly_pick.html", {
        "current_pick": current_pick,
        "past_picks": past_picks
    })

def album_list(request):
    query = request.GET.get('q', '')
    if query:
        albums = Album.objects.filter(
            Q(artist__icontains=query) |
            Q(title__icontains=query) |
            Q(genre__icontains=query) |
            Q(submitted_by__icontains=query)
        ).order_by('artist', 'title')
    else:
        albums = Album.objects.all().order_by('artist', 'title')
    
    # Check if this is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('albums/_album_table.html', {'albums': albums})
        return HttpResponse(html)
    
    return render(request, 'albums/album_list.html', {'albums': albums, 'query': query})


@login_required
def submit_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)  # Don't save yet
            album.submitted_by = request.user  # Assign logged-in user
            album.save()  # Now save
            return redirect('album_list')
    else:
        form = AlbumForm()
    
    return render(request, 'albums/submit_album.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # or wherever you'd like to send them
    else:
        form = UserCreationForm()
    
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    user_albums = Album.objects.filter(submitted_by=request.user)  # Get only their albums
    return render(request, 'accounts/profile.html', {'user': request.user, 'albums': user_albums})
