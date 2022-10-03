import datetime
import mutagen

from django.db import models
from googletrans import LANGUAGES


class Transcription(models.Model):
    """
    Model that describe an audio file.
    """
    name = models.CharField(max_length=200)
    audio = models.FileField(upload_to='uploads/%Y/%m/%d')
    language = models.CharField(max_length=8, choices=list(LANGUAGES.items()), default='en')
    duration = models.PositiveSmallIntegerField()

    text = models.TextField()

    create_datetime = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    transcribed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        audio_info = mutagen.File(self.audio).info
        self.duration = int(audio_info.length)

        super(Transcription, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-last_edit', '-create_datetime']
