from StringIO import StringIO
import os

from PIL import Image

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

from base import models as base_models

from . import conf as photo_gallery_conf

# Create your models here.


class Album(base_models.FullSlugBaseModel):
    url_name = photo_gallery_conf.NAMESPACE+":"+photo_gallery_conf.LIST_PHOTO_URL_NAME



class Photo(base_models.FullSlugBaseModel):

    url_name = photo_gallery_conf.NAMESPACE+":"+photo_gallery_conf.DETAIL_PHOTO_URL_NAME

    album_fk = models.ForeignKey(Album)
    photo_image = models.ImageField(upload_to='upload_images')
    thumbnail_100 = models.ImageField(upload_to='upload_images', blank=True, null=True)
    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.photo_image:
            return

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (100, 100)

        DJANGO_TYPE = self.photo_image.file.content_type

        PIL_TYPE = ""
        FILE_EXTENSION = ""

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.photo_image.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.photo_image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail_100.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):

        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Photo, self).save(force_update=force_update)


