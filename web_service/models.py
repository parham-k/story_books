import os

from django.db import models

from story_books_server.settings import BASE_DIR
from web_service import model_filenames


class Book(models.Model):
    title = models.CharField(
        max_length=255,
    )
    cover = models.ImageField(
        upload_to=model_filenames.get_book_cover_filename,
        storage=model_filenames.OverwriteStorage(),
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    def get_dir_path(self):
        return os.path.join(BASE_DIR, 'upload', 'books', self.title)

    def get_zip_filename(self):
        return '{}.zip'.format(os.path.join(self.get_dir_path(), self.title))

    def get_dict(self):
        data = {
            'title': self.title,
            'cover': self.cover.url,
            'date_added': self.date_added.isoformat(),
        }
        pages = dict()
        for page in self.pages.all():
            pages.update({page.number: {
                'text': page.text,
                'image': page.image.url,
                'audio': page.audio.url,
            }})
        data.update({'pages': pages})
        return data

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
    )
    audio = models.FileField(
        upload_to=model_filenames.get_page_audio_filename,
        storage=model_filenames.OverwriteStorage(),
    )
    text = models.CharField(
        max_length=8192,
    )
