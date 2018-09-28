from rest_framework import routers

from web_service import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('all_books', views.AllBooksViewSet)
