from celery import shared_task
from django.core.mail import mail_admins
from django.urls import reverse_lazy

from ghost_base_folder import settings
from transcribe.models import Transcription


@shared_task(ignore_result=True)
def async_audio_conversion(transcription_pk):
    transcription = Transcription.objects.get(pk=transcription_pk)
    transcription.convert_audio_to_mp3()


@shared_task(ignore_result=True)
def async_send_notification(transcription_pk):
    transcription = Transcription.objects.get(pk=transcription_pk)
    transcription_url = reverse_lazy(
        'admin:transcribe_transcription_change', args=(transcription_pk,)
    )
    subject = 'New audio uploaded'
    msg = (
        f'New audio uploaded by {transcription.user.username}.\n'
        f'- Name: {transcription.name}\n'
        f'- Language: {transcription.language}\n'
        f'- Audio duration: {transcription.readable_duration}\n'
        f'- Audio: {settings.SITE_URL}{transcription_url}\n'
    )

    mail_admins(
        subject,
        msg,
    )
