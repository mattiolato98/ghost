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
    context_object_name = 'audios'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(TranscriptionListView, self).get(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        return Transcription.objects.get(pk=pk) if pk is not None else None

    def get_context_data(self, **kwargs):
        context = super(TranscriptionListView, self).get_context_data(**kwargs)
        context['audio_object'] = self.object
        return context
