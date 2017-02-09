from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Interest(models.Model):
    title = models.CharField(max_length=50)
    keywords = models.TextField()
    pub_date = models.DateTimeField()
    num_of_imports = models.IntegerField(default=1)
    creator = models.ForeignKey(User, related_name='creator')
