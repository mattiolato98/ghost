import datetime
import os
from pathlib import Path

import mutagen
import pytz
from django.contrib.auth import get_user_model
from django.utils import formats
from googletrans import LANGUAGES
from django.core.files import File
from django.db import models

from ghost_base_folder.settings import MEDIA_ROOT
import transcribe.utils as audio_utils

import bleach as bleach
from bleach.css_sanitizer import CSSSanitizer
from tinymce.models import HTMLField


class Transcription(models.Model):
    """Model that represents an audio file and its transcription."""
    name = models.CharField(max_length=200)
    audio = models.FileField(upload_to='uploads/%Y/%m/%d')
    language = models.CharField(max_length=8, choices=list(LANGUAGES.items()), default='en')
    duration = models.PositiveSmallIntegerField()

    text = HTMLField(blank=True, null=True)

    create_datetime = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transcriptions')

    is_mp3 = models.BooleanField(default=False)
    transcribed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} of {self.user.username}'

    def clean(self):
        """Clean the message field from unauthorized tags.
        This prevents errors in visualization when the message is rendered in the frontend.
        """
        if self.text is not None:
            tags = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'pre', 'p', 'br', 'span', 'code', 'em',
                'i', 'li', 'ol', 'strong', 'ul', 'b', 'abbr'
            ]
            attrs = {
                '*': ['style'],
                'abbr': ['title'],
            }
            css_sanitizer = CSSSanitizer(allowed_css_properties=['background-color', 'text-align'])

            self.message = bleach.clean(self.text,
                                        tags=tags,
                                        attributes=attrs,
                                        css_sanitizer=css_sanitizer,
                                        strip=True)

        super(Transcription, self).clean()

    def save(self, *args, **kwargs):
        """Saves the audio duration in the model field before saving
        effectively the object.
        """
        if not self.pk:
            # execute only on create
            audio_info = mutagen.File(self.audio).info
            self.duration = int(audio_info.length)

        super(Transcription, self).save(*args, **kwargs)

    @classmethod
    def delete_expired_transcriptions(cls):
        """Asynchronous function that removes all the transcriptions
        objects which expiration date is, actually, expired.
        """
        for obj in cls.objects.all():
            if obj.days_to_expiration <= 0:
                obj.delete()

    @property
    def readable_duration(self):
        return formats.time_format(datetime.datetime.fromtimestamp(self.duration), 'H:i:s')

    @property
    def text_words(self):
        """Returns the number of words in a text."""
        return len(self.text.split()) if self.text is not None else 0

    @property
    def audio_path(self):
        """Returns the path of the transcription's audio."""
        return f'{MEDIA_ROOT}/{self.audio.name}'

    @property
    def audio_directory(self):
        """Returns the directory that contains the transcription's
        audio.
        """
        return os.path.dirname(self.audio.name)

    @property
    def audio_filename(self):
        """Return the audio filename without extension, if present."""
        if '.' in os.path.basename(self.audio.name):
            return os.path.basename(self.audio.name).rsplit('.', 1)[0]

        return os.path.basename(self.audio.name)

    @property
    def expiration_datetime(self):
        return self.create_datetime + datetime.timedelta(days=14)

    @property
    def days_to_expiration(self):
        return (self.expiration_datetime - datetime.datetime.now(tz=pytz.UTC)).days

    def create_audio_path(self, filename):
        """Creates an os path for a new transcription's audio."""
        return f'{MEDIA_ROOT}/{self.audio_directory}/{filename}'

    def update_audio_object(self, audio_path):
        """Updates the file object representing the transcription's
        audio, then the original file is removed since Django
        duplicates it.
        """
        new_path = Path(audio_path)
        with new_path.open(mode='rb') as f:
            self.audio = File(f, name=new_path.name)
            self.is_mp3 = True
            self.save()

        # removing the original copy of the file (duplicated by Django)
        audio_utils.remove_audio(audio_path)

    def convert_audio_to_mp3(self):
        """Asynchronous function that converts an uploaded audio file
        to the standard mp3 format.
        """
        old_audio_path = self.audio_path

        new_audio_filename = f'{self.audio_filename}.mp3'
        new_audio_path = self.create_audio_path(new_audio_filename)

        print(f'Converting asynchronously {old_audio_path} into {new_audio_path}')
        audio_utils.ffmpeg_conversion(old_audio_path, new_audio_path)
        # removing the old audio file
        audio_utils.remove_audio(old_audio_path)
        # saving the new file in the audio FileField
        self.update_audio_object(new_audio_path)

    class Meta:
        ordering = ['-last_edit', '-create_datetime']
