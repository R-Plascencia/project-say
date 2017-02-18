from django.db import models
from django.contrib.auth.models import User
from interests.models import Interest
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    interests = models.ManyToManyField(Interest)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username) #We do username = email address

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
# post_save.connect(create_profile, sender=User)
