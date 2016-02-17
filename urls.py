from django.conf.urls import url

from . import conf as photo_gallery_conf
from .views import album as album_views
from .views import photo as photo_views
urlpatterns = [
    url(
        r'^$',
        album_views.List.as_view(),
        name=photo_gallery_conf.LIST_ALBUM_URL_NAME
    ),
    url(
        r'^create/$',
        album_views.Create.as_view(),
        name=photo_gallery_conf.CREATE_ALBUM_URL_NAME
    ),

    url(
        r'^(?P<album_slug>[\w-]+)/$',
        photo_views.List.as_view(),
        name=photo_gallery_conf.LIST_PHOTO_URL_NAME
    ),
    url(
        r'^(?P<album_slug>[\w-]+)/create/$',
        photo_views.Create.as_view(),
        name=photo_gallery_conf.CREATE_PHOTO_URL_NAME
    ),
    url(
        r'^(?P<album_slug>[\w-]+)/create-multiple/$',
        photo_views.CreateMultiple.as_view(),
        name=photo_gallery_conf.CREATE_MULTIPLE_PHOTO_URL_NAME
    ),
]
