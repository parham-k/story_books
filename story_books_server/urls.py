from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from story_books_server import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_service.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
