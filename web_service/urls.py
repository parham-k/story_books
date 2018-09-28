from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import routers

from web_service import views

router = routers.DefaultRouter()
router.register(r'all_books', views.AllBooksViewSet, base_name='Book')

urlpatterns = [
    path('', include(router.urls)),
    path('get_auth_token/', obtain_auth_token)
]
