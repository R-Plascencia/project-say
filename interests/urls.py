from django.conf.urls import url
from . import views

app_name = 'interests'

urlpatterns = [
    url(r'^create/', views.create, name="create"),
]
