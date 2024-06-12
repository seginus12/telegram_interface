from django.db import models

# Create your models here.

class Poll(models.Model):
    poll_telegram_id = models.BigIntegerField()
    question = models.CharField(max_length=128)
    points = models.PositiveIntegerField()
    correct_option_id = models.PositiveIntegerField()

    def __repr__(self):
            return self.poll_name


class User(models.Model):
    user_telegram_id = models.BigIntegerField()
    username = models.CharField(max_length=64)
    total_points = models.PositiveIntegerField()

    def __repr__(self):
        return self.poll_name


class PollAnswer(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)