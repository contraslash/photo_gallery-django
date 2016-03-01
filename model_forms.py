from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models as photo_gallery_models
from . import conf as photo_gallery_conf


class Album(forms.ModelForm):

    class Meta:
        model = photo_gallery_models.Album
        fields = (
            'name',
            'description',
        )
        labels = {
            'name': _('Name'),
            'description': _('Description'),
        }

        widgets = {
            'name': forms.TextInput(attrs={'required': 'required'}),
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea',
            }),
        }


class Photo(forms.ModelForm):

    class Meta:
        model = photo_gallery_models.Photo
        fields = (
            'name',
            'description',
            'photo_image',
        )
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'photo_image': _('Photo'),
        }

        widgets = {
            'name': forms.TextInput(attrs={'required': 'required'}),
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea',
            }),
        }

class MultiplePhoto(forms.ModelForm):

    class Meta:
        model = photo_gallery_models.Photo
        fields = (
            'photo_image',
        )
