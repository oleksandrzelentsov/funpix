from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField


class Image(models.Model):
    title = models.TextField(max_length=32)
    image = models.ImageField(upload_to='images')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return '%i-%s' % (self.id, self.image.name)


class PixUser(User):
    # images published by user
    images = ManyToManyField(Image, blank=True, related_name='images_published')
    # images the user liked
    likes = ManyToManyField(Image, blank=True, related_name='liked_images')
