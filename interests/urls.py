from django.conf.urls import url
from . import views

app_name = 'interests'

urlpatterns = [
    url(r'^create/', views.create, name="create"),
    url(r'^list/', views.list, name="list"),
    url(r'^(?P<pk>[0-9]+)/copy', views.copy, name="copy"),
]
