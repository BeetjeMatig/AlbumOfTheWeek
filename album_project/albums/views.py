from datetime import date, timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import AlbumForm
from .lastfm import get_top_tag, search_albums
from .models import Album, WeeklyPick


def home(request):
    """Home page displaying the current week's album pick."""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Get Monday of the current week
    week_end = week_start + timedelta(days=6)  # Sunday of the current week

    weekly_pick = WeeklyPick.objects.order_by('-week_start_date').first()
    return render(request, 'albums/home.html', {'weekly_pick': weekly_pick})


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Review, WeeklyPick


def weekly_pick(request):
    weekly_pick = WeeklyPick.objects.order_by('-week_start_date').first()
    return render(request, 'albums/weekly_pick.html', {'weekly_pick': weekly_pick})

def view_reviews(request):
    pick_id = request.GET.get("pick")
    if pick_id:
        weekly_pick = get_object_or_404(WeeklyPick, id=pick_id)
    else:
        weekly_pick = WeeklyPick.objects.order_by('-week_start_date').first()

    reviews = Review.objects.filter(weekly_album=weekly_pick) if weekly_pick else None
    return render(request, 'albums/view_reviews.html', {'weekly_pick': weekly_pick, 'reviews': reviews})


@login_required
def write_review(request):
    from django.http import HttpResponseRedirect
    from django.urls import reverse

    pick_id = request.GET.get("pick")
    if pick_id:
        weekly_pick = get_object_or_404(WeeklyPick, id=pick_id)
    else:
        weekly_pick = WeeklyPick.objects.order_by('-week_start_date').first()

    if not weekly_pick:
        return redirect('weekly_pick')

    existing_review = Review.objects.filter(weekly_album=weekly_pick, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.weekly_album = weekly_pick
            review.user = request.user
            review.save()
            return HttpResponseRedirect(f"{reverse('view_reviews')}?pick={weekly_pick.id}")
    else:
        form = ReviewForm(instance=existing_review)  # 🔥 THIS fixes the error

    return render(request, 'albums/write_review.html', {
        'form': form,
        'weekly_pick': weekly_pick,
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
            album = form.save(commit=False)
            album.submitted_by = request.user
            album.save()
            return redirect('profile')
    else:
        form = AlbumForm()

    query = request.GET.get("q")
    search_results = []

    if query:
        try:
            search_results = search_albums(query)
        except Exception as e:
            print("Last.fm search error:", e)

    return render(request, 'albums/submit_album.html', {
        'form': form,
        'search_results': search_results,
        'query': query,
    })


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
    albums = Album.objects.filter(submitted_by=request.user)

    user_reviews = Review.objects.filter(user=request.user)
    reviewed_ids = user_reviews.values_list('weekly_album_id', flat=True)
    unreviewed_picks = WeeklyPick.objects.exclude(id__in=reviewed_ids).order_by('-week_start_date')

    return render(request, 'accounts/profile.html', {
        'albums': albums,
        'unreviewed_picks': unreviewed_picks,
    })


def previous_picks(request):
    picks = WeeklyPick.objects.order_by('-week_start_date')  # Most recent first
    return render(request, 'albums/previous_picks.html', {'picks': picks})
