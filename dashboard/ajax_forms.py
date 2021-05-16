from django import forms
from django.contrib.auth import get_user_model

from .models import Tag


class AddTagForm(forms.Form):
    name = forms.CharField(max_length=20)
    description = forms.CharField(max_length=100, required=False)

    def save(self, user) -> Tag:
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']

        tag = Tag.objects.create(name=name,
                                 owner=user,
                                 description=description)
        print(tag)
        return tag
