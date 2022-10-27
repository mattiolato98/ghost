from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from django import forms
from django.utils.translation import gettext_lazy as _

from transcribe.models import Transcription


class TranscriptionCreateForm(forms.ModelForm):
    """
    Form to upload an audio file.
    """
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(TranscriptionCreateForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(
                Column(FloatingField('name'), css_class='form-group col-12 col-lg-9'),
                Column(FloatingField('language'), css_class='form-group col-12 col-lg-3'),
                css_class='form-row'
            ),
            Row(
                Column(Field('audio', css_class='form-control-lg'), css_class='form-group col'),
                Column(
                    Submit(
                        'submit',
                        _('Transcribe'),
                        css_class='btn btn-lg site-btn w-auto font-5 px-5 px-lg-3 px-xxl-5 mt-3'
                    ),
                    css_class='col-12 col-lg-3 d-flex align-items-center justify-content-end mobile-center'
                ),
                css_class='form-row gap-3'
            ),
        )

    class Meta:
        model = Transcription
        fields = (
            'name',
            'language',
            'audio',
        )
        labels = {
            'name': _('Name'),
            'language': _('Language'),
            'audio': _('Audio'),
        }
        widgets = {
            'language': forms.Select(),
            'audio': forms.ClearableFileInput(attrs={'type': 'file', 'accept': 'audio/*'}),
        }


class TranscriptionUpdateForm(forms.ModelForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(TranscriptionUpdateForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(
                Column(FloatingField('name'), css_class='form-group col-12'),
                css_class='form-row justify-content-center'
            ),
            Row(
                Column('text', css_class='form-group col-10 mt-5'),
                css_class='form-row justify-content-center'
            ),
            Row(
                Column(
                    Submit(
                        'submit',
                        _('Save changes'),
                        css_class='btn site-btn w-auto font-5 white-space-normal'
                    ),
                    css_class='col d-flex justify-content-end mobile-center mt-3'
                ),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Transcription
        fields = (
            'name',
            'text',
        )
        labels = {
            'name': _('Name'),
            'text': '',
        }
