from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.template.loader import get_template
from django.utils.text import slugify
from django.core.urlresolvers import reverse_lazy

from base import views as base_views

from utils import utils

from .. import model_forms as photo_gallery_model_forms
from .. import models as photo_gallery_models
from .. import conf as photo_gallery_conf
# Create your views here.


class Create(base_views.BaseCreateView):
    form_class = photo_gallery_model_forms.Photo
    album = None

    def dispatch(self, request, *args, **kwargs):
        print self.kwargs
        try:
            self.album = photo_gallery_models.Album.objects.get(slug=self.kwargs.get('album_slug', 0))
            return super(Create, self).dispatch(request, *args, **kwargs)
        except photo_gallery_models.Album.DoesNotExist:
            return HttpResponseNotFound(get_template("404.html").render())

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.slug = slugify(utils.generate_random_string(5)+photo.name)
        photo.album_fk = self.album
        photo.save()
        return HttpResponseRedirect(
            reverse_lazy(
                photo_gallery_conf.NAMESPACE+":"+photo_gallery_conf.LIST_PHOTO_URL_NAME,
                kwargs={
                    'album_slug': self.album.slug
                }
            )
        )


class List(base_views.BaseGridView):
    template_name = "photo_gallery/photos/list.html"
    album = None

    def dispatch(self, request, *args, **kwargs):
        print self.kwargs
        try:
            self.album = photo_gallery_models.Album.objects.get(slug=self.kwargs.get('album_slug', 0))
            return super(List, self).dispatch(request, *args, **kwargs)
        except photo_gallery_models.Album.DoesNotExist:
            return HttpResponseNotFound(get_template("404.html").render())

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)

        context['album'] = self.album

        return context

    def get_queryset(self):
        return photo_gallery_models.Photo.objects.filter(album_fk=self.album)
