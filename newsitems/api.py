from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from .models import NewsItem, NewsResult

class NewsItemResource(ModelResource):
    class Meta:
        queryset = NewsItem.objects.all()
        resource_name = 'news_item'
        excludes = ['source']
        authorization = Authorization()

class NewsResultResource(ModelResource):
    interest = fields.OneToOneField('interests.api.InterestResource', 'interest')
    news_items = fields.ToManyField(NewsItemResource, 'newsitems', full=True)
    class Meta:
        queryset = NewsResult.objects.all()
        resource_name = 'news_results'
        authorization = Authorization()
