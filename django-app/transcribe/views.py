import celery

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from transcribe.decorators import transcription_owner_only
from transcribe.forms import TranscriptionCreateForm, TranscriptionUpdateForm
from transcribe.models import Transcription

from transcribe import utils as audio_utils


class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Transcription
    form_class = TranscriptionCreateForm
    template_name = 'transcribe/transcription_create.html'
    success_url = reverse_lazy('transcribe:transcription-list')

    def form_valid(self, form):
        """This function performs the following tasks:
        - testing if the uploaded file is an audio or not;
        - sending an email to the admins when a new audio is uploaded;
        - converting an audio file to MP3 if needed;
        """
        def not_audio_raise_error():
            not_audio_file_error_msg = _(
                'Only audio file supported. Please try again with an audio file.'
            )
            form.add_error("audio", error=not_audio_file_error_msg)
            return self.form_invalid(form)

        # depending on the file size, the audio can be temporarily
        # stored in a temporary file or in memory, so both the two
        # conditions should be handled:
        try:
            is_audio, audio_format = audio_utils.audio_info(
                form.cleaned_data['audio'].temporary_file_path()
            )
            if not is_audio:
                return not_audio_raise_error()
        except AttributeError:
            is_audio, audio_format = audio_utils.audio_info(
                form.cleaned_data['audio'].file, in_memory=True
            )
            if not is_audio:
                return not_audio_raise_error()

        # assigning current user to the object
        form.instance.user = self.request.user
        form.instance.is_mp3 = True if audio_format == 'mp3' else False

        self.object = form.save()

        celery.current_app.send_task(
            'transcribe.tasks.async_send_notification',
            args=(self.object.pk,),
        )
        if not form.instance.is_mp3:
            celery.current_app.send_task(
                'transcribe.tasks.async_audio_conversion',
                args=(self.object.pk,),
            )

        return super(TranscriptionCreateView, self).form_valid(form)


@method_decorator((login_required, transcription_owner_only), name='dispatch')
class TranscriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transcription
    template_name = 'transcribe/transcription_update.html'
    form_class = TranscriptionUpdateForm

    def get_success_url(self):
        return reverse_lazy('transcribe:transcription-list', kwargs={'pk': self.kwargs['pk']})


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


@method_decorator((login_required, transcription_owner_only), name='dispatch')
class TranscriptionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'transcribe/transcription_delete.html'
    success_url = reverse_lazy('transcribe:transcription-list')
    model = Transcription
