from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Bookings,Movies, Shows
from django.utils.translation import gettext as _



class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['no_of_tickets']

class addMovieForm(forms.ModelForm):
    class Meta:
        model=Movies
        fields = '__all__'
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

class addShowsForm(forms.ModelForm):
    class Meta:
        model=Shows
        fields = '__all__'
        widgets = {
            'show_date': forms.DateInput(attrs={'type': 'date'}),
        }



   
