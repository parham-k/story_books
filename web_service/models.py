from django.db import models

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
