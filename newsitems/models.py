from django.db import models
from interests.models import Interest

# Create your models here.
class NewsItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(max_length=300)
    top_img = models.URLField(max_length=300, default='')
    source = models.CharField(max_length=40, default='N/A')

    def __str__(self):
        return self.title

class NewsResult(models.Model):
    interest = models.OneToOneField(Interest, on_delete=models.CASCADE, related_name='newsresults')
    newsitems = models.ManyToManyField(NewsItem)

    def __str__(self):
        return "Results for {}".format(self.interest.title)
