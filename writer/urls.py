from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.writer_list, name='writers'),
    path('/add_writer', views.add_writer, name='add_writer'),
    path('/edit_writer/<int:id>/', views.edit_writer, name='edit_writer'),
    path('/delete_writer/<int:id>/', views.delete_writer, name='delete_writer'),
    path('/publisher_of_writers', views.publisher_of_writers, name='publisher_of_writers'),
]
