from django.shortcuts import render
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from base import views as base_views

from utils import utils

from .. import model_forms as photo_gallery_model_forms
from .. import models as photo_gallery_models
from .. import conf as photo_gallery_conf
# Create your views here.
class CreateAlbum(base_views.BaseCreateView):
    form_class = photo_gallery_model_forms.Album

    def get_context_data(self, **kwargs):
        context = super(CreateAlbum, self).get_context_data(**kwargs)
        print("CREATE ALBUM")
        return context

    def form_valid(self, form):
        album = form.save(commit=False)
        album.slug = slugify(utils.generate_random_string(4)+album.name)
        album.save()
        return HttpResponseRedirect(
            reverse_lazy(
                photo_gallery_conf.NAMESPACE+":"+photo_gallery_conf.LIST_ALBUM_URL_NAME
            )
        )


class ListAlbums(base_views.BaseGridView):
    template_name = "photo_gallery/album/list.html"
    queryset = photo_gallery_models.Album.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ListAlbums, self).get_context_data(**kwargs)
        print("LIST ALBUM")
        return context
