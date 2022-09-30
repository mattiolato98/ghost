from django.urls import reverse_lazy
from django.views.generic import CreateView

from transcribe.forms import AudioForm
from transcribe.models import Transcription


class TranscriptionCreateView(CreateView):
    model = Transcription
    form_class = AudioForm
    template_name = 'transcribe/transcribe.html'
    success_url = reverse_lazy('transcribe:transcribe')

