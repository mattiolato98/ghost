from django.db import models


class Stats(models.Model):
    unsubscribed_users = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Stats'
