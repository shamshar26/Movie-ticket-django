from django.contrib import admin
from .models import Movies, Shows, Bookings
# Register your models here.

class MoviesAdmin(admin.ModelAdmin):
    list_display=('movie_name','description','release_date')

admin.site.register(Movies,MoviesAdmin)

class ShowsAdmin(admin.ModelAdmin):
    list_display=('movie','show_time','is_disabled')

admin.site.register(Shows,ShowsAdmin)

class BookingsAdmin(admin.ModelAdmin):
    list_display=('user','show','booking_date','booking_id','is_confirmed')

admin.site.register(Bookings,BookingsAdmin)
