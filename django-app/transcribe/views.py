import celery
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from transcribe.forms import AudioForm
from transcribe.models import Transcription


class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Transcription
    form_class = AudioForm
    template_name = 'transcribe/transcription_form.html'
    success_url = reverse_lazy('transcribe:transcription-list')

    def form_valid(self, form):
        self.object = form.save()

        celery.current_app.send_task(
            'transcribe.tasks.async_audio_conversion',
            args=(self.object.pk,),
        )
        return HttpResponseRedirect(self.get_success_url())


class TranscriptionListView(LoginRequiredMixin, ListView):
    model = Transcription
    template_name = 'transcribe/transcription_list_and_detail.html'
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
