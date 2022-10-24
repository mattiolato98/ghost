from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class PlatformUserCreationForm(UserCreationForm):
    helper = FormHelper()
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None

        privacy_policy_url = reverse_lazy('user_management:privacy-policy')
        cookie_policy_url = reverse_lazy('user_management:cookie-policy')

        self.fields['privacy_and_cookie_policy_acceptance'].label = mark_safe(_(
            "I agree with the <strong><a href='{}' target='_blank' class='site-link'>"
            "privacy policy</a></strong> and the use of essential cookies, according "
            "with our <strong><a href='{}' target='_blank' class='site-link'>cookie "
            "policy</a></strong>, in order to allow the proper operation of the app"
        ).format(privacy_policy_url, cookie_policy_url))

        self.helper.layout = Layout(
            Row(
                Column(FloatingField('username'), css_class='form-group mb-0'),
                Column(FloatingField('email'), css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(FloatingField('password1'), css_class='form-group'),
                Column(FloatingField('password2'), css_class='form-group'),
                css_class='form-row',
            ),
            Row(
                Column('privacy_and_cookie_policy_acceptance', css_class='form-group'),
                css_class='form-row'
            ),
        )

    def clean(self):
        if not self.cleaned_data['privacy_and_cookie_policy_acceptance']:
            raise ValidationError(_("You must accept the privacy policies."))

        return super(PlatformUserCreationForm, self).clean()

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'privacy_and_cookie_policy_acceptance',
        )


class LoginForm(AuthenticationForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Row(
                Column(FloatingField('username'), css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(FloatingField('password'), css_class='form-group mb-0'),
                css_class='form-row'
            )
        )
