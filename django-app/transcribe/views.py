import celery

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView

from transcribe.forms import AudioForm
from transcribe.models import Transcription

from transcribe import utils as audio_utils


class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Transcription
    form_class = AudioForm
    template_name = 'transcribe/transcription_form.html'
    success_url = reverse_lazy('transcribe:transcription-list')

    def form_valid(self, form):
        def not_audio_raise_error():
            not_audio_file_error_msg = _('Only audio file supported. Please try again with an audio file.')
            form.add_error("audio", error=not_audio_file_error_msg)
            return self.form_invalid(form)

        try:
            is_audio, audio_format = audio_utils.audio_info(form.cleaned_data['audio'].temporary_file_path())
            if not is_audio:
                return not_audio_raise_error()
        except AttributeError:
            return not_audio_raise_error()

        # assigning current user to the object
        form.instance.user = self.request.user
        form.instance.is_mp3 = True if audio_format == 'mp3' else False

        self.object = form.save()

        celery.current_app.send_task(
            'transcribe.tasks.async_audio_conversion',
            args=(self.object.pk,),
        )
        return HttpResponseRedirect(self.get_success_url())


class TranscriptionListView(LoginRequiredMixin, ListView):
    model = Transcription
    template_name = 'transcribe/transcription_list_and_detail.html'
    context_object_name = 'transcriptions'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(TranscriptionListView, self).get(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        return Transcription.objects.get(pk=pk) if pk is not None else None

    def get_queryset(self):
        return Transcription.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TranscriptionListView, self).get_context_data(**kwargs)
        context['transcription_object'] = self.object
        return context
