from django.views.generic import TemplateView


class TranscribeView(TemplateView):
    template_name = "transcribe/transcribe.html"
