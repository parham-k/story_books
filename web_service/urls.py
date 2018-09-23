from django.urls import path

from web_service import views

urlpatterns = [
    path('get_book/<int:id>/', views.get_book),
    path('get_latest_books', views.get_latest_books),
]
