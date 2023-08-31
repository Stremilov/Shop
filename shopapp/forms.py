from django.forms import ModelForm
from django.contrib.auth.models import Group

from .models import Models


class ProductCreate(ModelForm):
    class Meta:
        model = Models
        fields = 'name', 'price', 'description', 'discount', 'created_by'


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']