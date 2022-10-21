import os
from pathlib import Path

import mutagen
from googletrans import LANGUAGES
from django.core.files import File
from django.db import models

from ghost_base_folder.settings import MEDIA_ROOT
import utils.audio_utils as audio_utils


class Transcription(models.Model):
    """Model that represents an audio file and its transcription."""
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
        """Saves the audio duration in the model field before saving
        effectively the object.
        """
        audio_info = mutagen.File(self.audio).info
        self.duration = int(audio_info.length)

        super(Transcription, self).save(*args, **kwargs)

    @property
    def text_words(self):
        """Returns the number of words in a text."""
        return len(self.text.split())

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
            self.save()
        # removing the original copy of the file (duplicated by Django)
        audio_utils.remove_audio(audio_path)

    def convert_audio_to_mp3(self):
        """Asynchronous function that converts an uploaded audio file
        to the standard mp3 format
        """
        old_audio_path = self.audio_path

        if audio_utils.get_audio_format(self.audio_path) == 'mp3':
            return

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
