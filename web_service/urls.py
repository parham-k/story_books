from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from web_service.routers import router

urlpatterns = [
    path('', include(router.urls)),
    path('get_auth_token/', obtain_auth_token)
]
