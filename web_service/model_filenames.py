import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def get_book_text_filename(instance, filename):
    return os.path.join('upload', 'books', instance.title, 'text.txt')


def get_book_cover_filename(instance, filename):
    return os.path.join('upload', 'books', instance.title, 'cover.png')


def get_page_image_filename(instance, filename):
    return os.path.join('upload', 'books', str(instance.number), '{}.png'.format(instance.number))


def get_page_audio_filename(instance, filename):
    return os.path.join('upload', 'books', str(instance.number), '{}.mp3'.format(instance.number))
