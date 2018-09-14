from django.urls import path

from web_service import views

urlpatterns = [
    path('get_book/<str:title>/', views.get_book),
]
