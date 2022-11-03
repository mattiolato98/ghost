from django.db import models


class Stats(models.Model):
    unsubscribed_users = models.IntegerField(default=0)
