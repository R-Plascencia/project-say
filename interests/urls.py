from django.conf.urls import url, include
from . import views

app_name = 'interests'

urlpatterns = [
    url(r'^create/', views.create, name="create"),
    url(r'^list/', views.list, name="list"),
    url(r'^(?P<pk>[0-9]+)/copy', views.copy, name="copy"),
    url(r'^(?P<pk>[0-9]+)/refresh', views.refresh, name="refresh"),
    url(r'^(?P<pk>[0-9]+)/remove', views.remove, name="remove"),
]
