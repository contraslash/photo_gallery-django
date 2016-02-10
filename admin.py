from django.contrib import admin
from . import models as photo_gallery_models
# Register your models here.
admin.site.register(photo_gallery_models.Album)
admin.site.register(photo_gallery_models.Photo)
