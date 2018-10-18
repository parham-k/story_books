from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from web_service import model_filenames


class User(AbstractUser):
    full_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    books = models.ManyToManyField('Book', related_name='owners')

    def __str__(self):
        return self.phone


class Book(models.Model):
    title = models.CharField(
        max_length=255,
    )
    cover = models.ImageField(
        upload_to=model_filenames.get_book_cover_filename,
        storage=model_filenames.OverwriteStorage(),
        default='default_book_cover.png',
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )
    categories = ArrayField(models.CharField(max_length=16), blank=True, null=True)
    ages = models.CharField(max_length=32)
    summary = models.TextField(max_length=8192)
    author = models.CharField(max_length=64)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_added']


class Page(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='pages',
    )
    number = models.IntegerField()
    image = models.ImageField(
        upload_to=model_filenames.get_page_image_filename,
        storage=model_filenames.OverwriteStorage(),
        default='default_page_image.png',
    )
    audio = models.FileField(
        upload_to=model_filenames.get_page_audio_filename,
        storage=model_filenames.OverwriteStorage(),
        blank=True,
        null=True,
    )
    text = models.TextField(
        max_length=8192,
    )


class Slide(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='slides'
    )
    image = models.ImageField()


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        max_length=1024,
    )
    date = models.DateTimeField(
        auto_now_add=True,
    )
    approved = models.BooleanField(
        default=False,
    )


class AppInfo(models.Model):
    key = models.CharField(
        max_length=64
    )
    value = models.TextField(
        max_length=1024,
    )
