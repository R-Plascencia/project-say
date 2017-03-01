from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.NewsItem)
admin.site.register(models.NewsResult)
