from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from djng.styling.bootstrap3.forms import Bootstrap3Form
from .models import Interest
from djng.forms import NgFormValidationMixin, NgModelForm

# class InterestForm(Bootstrap3Form):
    # title = forms.CharField(label='Title', max_length=40, required=True)
    # keywords = forms.CharField(label='Keywords', max_length=100, required=True)


class InterestForm(NgFormValidationMixin, NgModelForm):
    class Meta:
         model = Interest
         fields = ['title', 'keywords']
