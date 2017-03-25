from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from .models import Interest
from accounts.api import UserResource

class InterestResource(ModelResource):
    creator = fields.ForeignKey(UserResource, 'creator', full=True)
    
    class Meta:
        queryset = Interest.objects.all()
        resource_name = 'interest'
        allowed_methods = ['get', 'post']
        always_return_data = True
        authorization = Authorization()