from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from transcribe.models import Transcription


class AudioForm(forms.ModelForm):
    """
    Form to upload an audio file.
    """
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(AudioForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('audio', css_class='form-group'),
                css_class='form-row',
            ),
            Row(
                Column(
                    Submit('submit', _('Insert'), css_class='btn site-btn mb-3 w-75 font-5'),
                    css_class='d-flex align-items-end justify-content-end'
                ),
                css_class='form-row '
            ),
        )

    class Meta:
        model = Transcription
        fields = (
            'name',
            'audio',
        )
        labels = {
            'name': _('Name'),
            'audio': _('Audio'),
        }
        widgets = {
            'audio': forms.ClearableFileInput(attrs={'type': 'file', 'accept': 'audio/*'}),
        }
