from django.db import models
from interests.models import Interest
from django.utils import timezone

# Create your models here.
class NewsItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    link = models.URLField(max_length=350)
    top_img = models.URLField(max_length=350, default='')
    source = models.CharField(max_length=40, default='N/A')
    keywords = models.CharField(max_length=100, default='')
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title

class NewsResult(models.Model):
    interest = models.OneToOneField(Interest, on_delete=models.CASCADE, related_name='newsresults')
    newsitems = models.ManyToManyField(NewsItem)

    def __str__(self):
        return "Results for {}".format(self.interest.title)
