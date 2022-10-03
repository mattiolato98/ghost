from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from transcribe.forms import AudioForm
from transcribe.models import Transcription


class TranscriptionCreateView(CreateView):
    model = Transcription
    form_class = AudioForm
    template_name = 'transcribe/transcription_form.html'
    success_url = reverse_lazy('transcribe:transcription-form')


class TranscriptionListView(ListView):
    model = Transcription
    template_name = 'transcribe/transcription_list.html'
