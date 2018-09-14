from os.path import join
from django.db import models

from story_books_server.settings import BASE_DIR


class Book(models.Model):
    title = models.CharField(
        max_length=255,
    )
    text = models.FileField(
        upload_to=lambda instance, filename: join(BASE_DIR, 'upload', 'books', instance.title, 'text.txt')
    )
    cover = models.ImageField(
        upload_to=lambda instance, filename: join(BASE_DIR, 'upload', 'books', instance.title, 'cover.png')
    )
