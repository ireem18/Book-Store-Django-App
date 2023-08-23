from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('create_user', views.create_user, name='create_user'),
]
