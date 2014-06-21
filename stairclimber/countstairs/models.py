from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DailyStairs(models.Model):
  	day = models.DateField('date climbed')
   	up = models.IntegerField(default=0)
   	down = models.IntegerField(default=0)
   	total = models.IntegerField(default=0)
   	climber = models.ForeignKey(User)

class UserPreferences(models.Model):
	user = models.OneToOneField(User)
	upDown = models.BooleanField()
	sendReport = models.BooleanField()

class CustomStairCount(models.Model):
	name = models.CharField(max_length=200)
	steps = models.IntegerField()
	user = models.ForeignKey(User)
	count = models.IntegerField(default=0)