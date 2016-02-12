from django.shortcuts import render
from django.utils.text import slugify
from django import http
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from base import views as base_views

from utils import utils

from .. import model_forms as photo_gallery_model_forms
from .. import models as photo_gallery_models
from .. import conf as photo_gallery_conf
# Create your views here.
class Create(base_views.BaseCreateView):
    form_class = photo_gallery_model_forms.Album

    @method_decorator(login_required(login_url='log_in'))
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('photo_gallery.add_album'):
            return super(Create, self).dispatch(request, *args, **kwargs)
        else:
            return http.HttpResponseForbidden(get_template("403.html"))

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        print("CREATE ALBUM")
        return context

    def form_valid(self, form):
        album = form.save(commit=False)
        album.slug = slugify(utils.generate_random_string(4)+album.name)
        album.save()
        return http.HttpResponseRedirect(
            reverse_lazy(
                photo_gallery_conf.NAMESPACE+":"+photo_gallery_conf.LIST_ALBUM_URL_NAME
            )
        )


class List(base_views.BaseGridView):
    template_name = "photo_gallery/album/list.html"
    queryset = photo_gallery_models.Album.objects.all()

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        print("LIST ALBUM")
        return context
