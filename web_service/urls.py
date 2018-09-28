from django.urls import path, include

from web_service.routers import router

urlpatterns = [
    path('', include(router.urls)),
]
