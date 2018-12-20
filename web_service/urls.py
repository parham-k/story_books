from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from web_service import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_token/', obtain_auth_token),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('shop/', views.shop, name='shop'),
    path('book_info/', views.book_info, name='book_info'),
    path('purchase/', views.purchase, name='purchase'),
    path('app_info/', views.get_app_info, name='app_info'),
    path('send_comment/', views.send_comment, name='send_comment'),
    path('send_feedback/', views.send_feedback, name='send_feedback'),
    path('payment/request/', views.payment_request, name='payment_request'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('edit_profile/', views.edit_profile, name='edit_profile')
    # TODO: path('activate/', views.activate_profile, name='activate_profile'),
]
