import os
import zipfile

from django.db import models
from django.dispatch import receiver

from story_books_server.settings import BASE_DIR
from web_service import model_filenames


class Book(models.Model):
    title = models.CharField(
        max_length=255,
    )
    text = models.FileField(
        upload_to=model_filenames.get_book_text_filename,
        storage=model_filenames.OverwriteStorage(),
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

    class Meta:
        ordering = ['-date_added']


@receiver(models.signals.post_save, sender=Book)
def create_zip_file(sender, instance, created, **kwargs):
    if os.path.exists(instance.get_zip_filename()):
        os.remove(instance.get_zip_filename())
    z = zipfile.ZipFile(instance.get_zip_filename(), 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(instance.get_dir_path()):
        for file in files:
            if os.path.join(root, file) != instance.get_zip_filename():
                z.write(os.path.join(root, file), file)
    z.close()
