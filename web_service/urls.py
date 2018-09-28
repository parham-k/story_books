from django.urls import path, include

from web_service import views
from web_service.routers import router

urlpatterns = [
    path('', include(router.urls)),
    path('get_book/<int:id>/', views.get_book),
    path('get_latest_books', views.get_latest_books),
]
