from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    contact = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    bankName = models.ForeignKey('Bank', on_delete=models.CASCADE, blank=True, null=True)
    accNo = models.CharField(max_length=20, blank=True, null=True)
    ifscNo = models.CharField(max_length=20, blank=True, null=True)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
