from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Album

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
