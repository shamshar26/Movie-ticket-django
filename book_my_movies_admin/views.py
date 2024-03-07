from django.shortcuts import render,redirect
from .models import Movies, Shows, Bookings
from django.contrib.auth.decorators import login_required
from .forms import addMovieForm,addShowsForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def home(request):
    movie=Movies.objects.all()
    show=Shows.objects.all()
    return render(request, 'home.html',{'show': show, 'movie':movie})
    

def adminLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/book_my_movies_admin/login')
def adminLogout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('adminLogin')
    return render(request, 'logged_out.html')

@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def addMovie(request):
    if request.method == 'POST':
        form = addMovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = addMovieForm()
    return render(request, 'movie_form.html', {'form': form})

@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def editMovie(request, pk):
    movie = Movies.objects.get(pk=pk)
    if request.method == 'POST':
        form = addMovieForm(request.POST,request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = addMovieForm(instance=movie)           
    return render(request, 'movie_form.html', {'form': form})

@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def movieDelete(request,pk):
    movie=Movies.objects.get(pk=pk)  
    if request.method == 'POST':
        movie.delete()
        return redirect('home')
    return render(request,'movie_confirm_delete.html',{'movie':movie})


@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def addShow(request):
    if request.method == 'POST':
        form = addShowsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = addShowsForm()
    return render(request, 'show_form.html', {'form': form})


@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def editShow(request, pk):
    show = Shows.objects.get(pk=pk)
    if request.method == 'POST':
        form = addShowsForm(request.POST,instance=show)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = addShowsForm(instance=show)           
    return render(request, 'show_form.html', {'form': form})


@login_required(login_url='/book_my_movies_admin/login')
@user_passes_test(is_admin, login_url='/book_my_movies_admin/login')
def deleteShow(request,pk):
    show=Shows.objects.get(pk=pk)  
    if request.method == 'POST':
        show.delete()
        return redirect('home')
    return render(request,'show_confirm_delete.html',{'show':show})
