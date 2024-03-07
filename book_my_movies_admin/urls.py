from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('login', views.adminLogin, name='adminLogin'),
    path('logout', views.adminLogout, name='adminLogout'),
    path('movies/add',views.addMovie,name='addMovie'),
    path('movies/<int:pk>/edit/',views.editMovie, name='editMovie'),
    path('movies/<int:pk>/delete/',views.movieDelete, name='deleteMovie'),
    path('shows/add',views.addShow,name='addShow'),
    path('shows/<int:pk>/edit/',views.editShow,name='editShow'),
    path('shows/<int:pk>/delete/',views.deleteShow,name='deleteShow'),
    
]