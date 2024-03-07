from django.urls import path
from . import views


urlpatterns = [
    path('register',views.register, name='register_api'),
    path('login', views.login, name='login_api'),
    path('logout', views.user_logout, name='logout_api'),
    path('movies',views.movieList,name='movieList'),
    path('shows/<int:movie_id>', views.showList, name='showList_api'),
    path('booking/<int:pk>', views.bookShow, name='bookShow'),
    path('booking/mybookings',views.myBookings,name='myBookings'),
    path('booking/confirmation/<int:id>', views.confirmation, name='confirmation_api'),
    path('generate_pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
]