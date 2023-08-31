from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def profile_preview_directory_path(instance, username):
    return 'users/user_{pk}/preview/{username}'.format(pk=instance.pk, username=username)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(null=True, blank=True, max_length=15)
    first_name = models.CharField(null=True, max_length=15)
    email = models.CharField(null=True, blank=True, max_length=30)
    bio = models.TextField(max_length=400, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_preview_directory_path)
