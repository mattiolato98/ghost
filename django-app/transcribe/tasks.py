from celery import shared_task

from transcribe.models import Transcription


@shared_task(ignore_result=True)
def async_audio_conversion(transcription_pk):
    transcription = Transcription.objects.get(pk=transcription_pk)
    if transcription.is_mp3:
        return

    transcription.convert_audio_to_mp3()
