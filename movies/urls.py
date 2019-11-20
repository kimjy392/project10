from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/detail/', views.detail, name='detail'),
    path('<int:movie_id>/reviews/new/', views.create, name='create'),
    path('<int:movie_id>/reviews/<int:review_id>/delete', views.delete, name='delete'),
    path('<int:movie_id>/like/', views.like, name='like')
]