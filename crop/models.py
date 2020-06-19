from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Types(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=100)
	value = models.IntegerField()

	def __str__(self):
		return self.name

class Crop(models.Model):
	farmer = models.OneToOneField(User, on_delete=models.CASCADE)
	cat = models.ForeignKey('Category', on_delete=models.CASCADE)
	name = models.ForeignKey('Types', on_delete=models.CASCADE)
	quantity = models.IntegerField()
	unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
	description = models.TextField(null=True, blank=True)
	pickup = models.CharField(max_length=200)
	image = models.ImageField(upload_to='crop', null=True, blank=True)
	date_posted = models.DateField(default=timezone.now)
	price = models.IntegerField(default=0)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True, default = None)

	def __str__(self):
		return f'{self.farmer} - {self.date_posted}'

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


class Bid(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
	value = models.CharField(max_length=10, default = None)
	stuff = models.ForeignKey(Crop, on_delete=models.CASCADE, default = None)

	def __str__(self):
		return f'{self.stuff.name}-{self.author.username}'

class Transaction(models.Model):
	farmer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer')
	buyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')

	def __str__(self):
		return f'{self.farmer.user.username} - {self.buyer.user.username}'

class Newsletter(models.Model):
	mail = models.EmailField()

	def __str__(self):
		return self.mail