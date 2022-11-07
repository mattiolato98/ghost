from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from transcribe.models import Transcription
from user_management.models import PlatformUser


def create_user():
    return PlatformUser.objects.create_user(
        username='test_user',
        email='test_user@example.com',
        password='password',
    )


def get_audio_content():
    return (b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04\x00'
            b'\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00')


class TranscriptionTests(TestCase):
    """Very dummy tests to make GitLab pipeline useful."""
    def setUp(self) -> None:
        self.test_audio = SimpleUploadedFile(
            name='test_audio.mp3', content=get_audio_content(), content_type='audio/*'
        )
        self.user = create_user()
        self.client = Client()

    def test_access_create_page(self):
        response = self.client.get(reverse('transcribe:transcription-form'))
        self.assertEqual(response.status_code, 302)  # user must be logged in first
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('transcribe:transcription-form'))
        self.assertEqual(response.status_code, 200)

    def test_transcription_creation(self):
        self.transcription = Transcription.objects.create(
            name='test_audio',
            audio=self.test_audio,
            user=self.user,
        )
        self.assertEqual(self.transcription.duration, 0)
