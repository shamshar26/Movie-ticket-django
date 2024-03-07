from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date,time

# Create your models here.

class Movies(models.Model):
    movie_name=models.CharField(max_length=100)
    description=models.TextField()
    release_date=models.DateField()
    movie_image=models.ImageField(upload_to='movie_images/',blank=False)

    def __str__(self):
        return self.movie_name

class Shows(models.Model):
    movie=models.ForeignKey(Movies, on_delete=models.CASCADE)
    show_date=models.DateField(default=timezone.now)
    TIME_CHOICES = [
        (time(11,30,00), '11:30 AM'),
        (time(14,30,00), '2:30 PM'),
        (time(17,00,00), '5:00 PM'),
        (time(21,00,00), '9:00 PM')
        ]
    show_time=models.TimeField(
        max_length=8,
        choices=TIME_CHOICES,
        blank=False,
    )
    is_disabled=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.movie.movie_name} {self.show_date} {self.show_time}'
    
    

class Bookings(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    show=models.ForeignKey(Shows, on_delete=models.CASCADE)
    no_of_tickets=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    booking_date=models.DateTimeField(auto_now_add=True)
    booking_id=models.CharField(max_length=20, unique=True, null=False, default='qwerty')
    is_confirmed=models.BooleanField(default=False)

    def calculate_total_amount(self):
        ticket_price = 100 
        return self.no_of_tickets * ticket_price
    
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



