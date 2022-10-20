import fleep
import mutagen
import os

from django.db import models
from googletrans import LANGUAGES
from ghost_base_folder.settings import MEDIA_ROOT


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

    @property
    def text_words(self):
        return len(self.text.split())

    def save(self, *args, **kwargs):
        """Saves the audio duration in the model field before saving
        effectively the object.
        """
        audio_info = mutagen.File(self.audio).info
        self.duration = int(audio_info.length)

        super(Transcription, self).save(*args, **kwargs)

        audio_filename, audio_extension = os.path.basename(self.audio.name).rsplit('.', 1)
        old_audio = f'{MEDIA_ROOT}/{self.audio.name}'

        with open(old_audio, 'rb') as file:
            info = fleep.get(file.read(128))

        audio_format = info.extension[0]

        if audio_format != 'mp3':
            new_audio_filename = f'{audio_filename}.mp3'
            new_audio = f'{MEDIA_ROOT}/{os.path.dirname(self.audio.name)}/{new_audio_filename}'

            os.system(f'ffmpeg -i {old_audio} -vn -ar 44100 -ac 2 -b:a 192k {new_audio}')
            os.system(f'rm {old_audio}')

    class Meta:
        ordering = ['-last_edit', '-create_datetime']
