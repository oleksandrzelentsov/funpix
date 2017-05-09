from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField


class PixUser(User):
    pictures = ManyToManyField(Picture)


class Picture(models.Model):
    title = models.TextField(max_length=32)
    picture = models.ImageField(upload_to='images')
    pluses = models.ManyToManyField(PixUser)

    def __str__(self):
        return '%s-%s' % (self.picture.name, self.token)
