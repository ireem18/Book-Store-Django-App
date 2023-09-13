from django.urls import path, include
from books import views

urlpatterns = [
    path('', views.book_list, name='books'),
    path('/chart_board', views.chart_board, name='chart_board'),
    path('/add_book', views.add_book, name='add_book'),
    path('/edit_book/<int:id>/', views.edit_book, name='edit_book'),
    path('/delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('/export_book_list', views.export_book_list, name='export_book_list'),
]
