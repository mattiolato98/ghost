from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
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
                Column(FloatingField('name'), css_class='form-group col-12 col-lg-9'),
                Column(FloatingField('language'), css_class='form-group col-12 col-lg-3'),
                css_class='form-row'
            ),
            Row(
                Column(Field('audio', css_class='form-control-lg'), css_class='form-group col-12 col-lg-9'),
                Column(
                    Submit('submit', _('Transcribe'), css_class='btn btn-lg site-btn w-auto font-5 px-sm-5 mt-3'),
                    css_class='col-12 col-lg-3 d-flex align-items-center justify-content-end mobile-center'
                ),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Transcription
        fields = (
            'name',
            'language',
            'audio',
        )
        widgets = {
            'language': forms.Select(),
            'audio': forms.ClearableFileInput(attrs={'type': 'file', 'accept': 'audio/*'}),
        }
