from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from .models import UserProfile

class UserProfileResource(ModelResource):
    user = fields.ToOneField('accounts.api.UserResource', 'user')
    interests = fields.ToManyField('interests.api.InterestResource', 'interests')
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'
        authorization = Authorization()

class UserResource(ModelResource):
    profile = fields.OneToOneField(UserProfileResource, 'profile', full=True)
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'resource_uri']
        authorization = Authorization()
