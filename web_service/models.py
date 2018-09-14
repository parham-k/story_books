from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=255,
    )
    text = models.FileField()
    cover = models.ImageField()
