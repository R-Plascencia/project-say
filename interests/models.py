from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Interest(models.Model):
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    last_refreshed = models.DateTimeField(default=timezone.now())
    num_of_imports = models.IntegerField(default=1)
    creator = models.ForeignKey(User, related_name='creator')

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def refresh_time_pretty(self):
        return self.last_refreshed.strftime('%b %e %Y')

@receiver(post_save, sender=Interest)
def create_results_bucket(sender, **kwargs):
    result_inst = kwargs["instance"]
    if kwargs["created"]:
        news_results = Interest(newsresult=result_inst)
        news_results.save()
