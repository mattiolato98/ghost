from django.db import models


class SignInToken(models.Model):
    token = models.CharField(max_length=16, unique=True)
    is_active = models.BooleanField(default=True)

    create_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        ordering = ['-create_datetime']
