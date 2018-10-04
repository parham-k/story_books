from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from web_service import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_token/', obtain_auth_token),
    path('signup/', views.signup, name='signup')
]
