from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField


class Image(models.Model):
    title = models.TextField(max_length=32)
    image = models.ImageField(upload_to='images')
    likes = models.ManyToManyField(User, related_name='likes_received', blank=True)
    author = models.ForeignKey(User, default=1)

    def __str__(self):
        return '%i-%s' % (self.id, self.image.name)

