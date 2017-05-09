from django.contrib import admin

# Register your models here.
from pix.models import Image, PixUser

admin.site.register(PixUser)
admin.site.register(Image)
