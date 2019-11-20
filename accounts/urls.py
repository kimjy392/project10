from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:user_id>/', views.detail, name='detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('following/<int:user_id>/', views.following, name='following')
]
