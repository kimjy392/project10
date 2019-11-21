from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserCustomForm
from movies.models import Movie

# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    return render(request, 'accounts/index.html', {'users': users})

import random
def detail(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    if user.like_movies.exists():
        genre = user.like_movies.all()[0].genre.movie_set.all()
        for movie in genre:
            if movie not in user.like_movies.all():
                recommand = movie
                break
        else:
            recommand = Movie.objects.all()[random.randint(0, 9)]
            while recommand in user.like_movies.all():
                recommand = Movie.objects.all()[random.randint(0, 9)]
    else:
        recommand = Movie.objects.all()[random.randint(0, 9)]
        while recommand in user.like_movies.all():
            recommand = Movie.objects.all()[random.randint(0, 9)]
    return render(request, 'accounts/detail.html', {'user': user, 'recommand':recommand})

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method=='POST':
        form = UserCustomForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = UserCustomForm()
    return render(request, 'accounts/forms.html', {'form':form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method=='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/forms.html', {'form':form})

def signout(request):
    if request.user.is_authenticated:
       auth_logout(request)
    return redirect('movies:index')

@login_required
def following(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    if request.user == user:
        return redirect('accounts:detail', user_id)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('accounts:detail', user_id)