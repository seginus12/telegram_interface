from django.db import models

# Create your models here.

class Poll(models.Model):
    points = models.IntegerField()
    telegram_id = models.IntegerField()

class User(models.Model):
    username = models.CharField(max_length=64)
    telegram_id = models.IntegerField()
    total_points = models.IntegerField()
