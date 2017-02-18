from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Interest(models.Model):
    title = models.CharField(max_length=50)
    keywords = models.TextField()
    pub_date = models.DateTimeField()
    num_of_imports = models.IntegerField(default=1)
    creator = models.ForeignKey(User, related_name='creator')

    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
