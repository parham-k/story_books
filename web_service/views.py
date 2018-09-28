from rest_framework import viewsets

from web_service import models, serializers


class AllBooksViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
