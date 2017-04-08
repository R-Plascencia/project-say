from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from .models import Interest
from accounts.api import UserResource
from newsitems.api import NewsResultResource

class InterestResource(ModelResource):
    creator = fields.ForeignKey(UserResource, 'creator', full=True)
    news_result = fields.OneToOneField(NewsResultResource, 'newsresults', null=True, full=True)
    class Meta:
        queryset = Interest.objects.all()
        resource_name = 'interest'
        allowed_methods = ['get', 'post']
        always_return_data = True
        authorization = Authorization()
