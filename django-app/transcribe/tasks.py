from celery import shared_task


@shared_task(ignore_result=True)
def async_convert_audio(transcription_pk):
    print("Hello World! I am an asynchronous task!")
