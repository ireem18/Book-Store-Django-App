from django.urls import path
from . import views

urlpatterns = [
    path('', views.publisher_list, name='publishers'),
    path('/add_publisher', views.add_publisher, name='add_publisher'),
    path('/edit_publisher/<int:id>/', views.edit_publisher, name='edit_publisher'),
    path('/delete_publisher/<int:id>/', views.delete_publisher, name='delete_publisher'),
]
