from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Movie, Review
from .forms import ReviewForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    return render(request, 'movies/index.html', {'movies' : movies})

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    form = ReviewForm()
    return render(request, 'movies/detail.html', {'movie' : movie, 'form':form})

@require_POST
def create(request, movie_id):
    if request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = get_object_or_404(Movie, pk=movie_id)
            review.save()
            return redirect('movies:detail', movie_id)
    else:
        return redirect('accounts:login')

@require_POST
def delete(request, movie_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_id)
        if review.user == request.user:
            review.delete()
    return redirect('movies:detail', movie_id)

@login_required
def like(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_id)
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
    return redirect('movies:detail', movie_id)

