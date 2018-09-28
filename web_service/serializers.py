from rest_framework import serializers

from web_service import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'full_name', 'phone')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = ('url', 'pk', 'title', 'date_added')
