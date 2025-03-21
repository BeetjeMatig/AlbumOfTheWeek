from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'genre', 'release_year']  # Removed 'submitted_by'

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'favorite_song', 'least_favorite_song']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 100, 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your review...'}),
            'favorite_song': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Favourite song'}),
            'least_favorite_song': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Least favourite song'}),
        }
