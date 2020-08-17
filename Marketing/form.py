from django import forms
from django.forms import modelform_factory
from django.forms import fields, widgets
from .models import Demands
from Operation.models import Product


class DemandForm(forms.ModelForm):
    class Meta:
        model = Demands
        fields='__all__'

