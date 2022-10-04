from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class PlatformUserCreationForm(UserCreationForm):
    helper = FormHelper()
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': _('Your email')})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Confirm password')})

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
                Column('username', css_class='form-group mb-0'),
                Column('email', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group'),
                Column('password2', css_class='form-group'),
                css_class='form-row',
            ),
            Row(
                Column('privacy_and_cookie_policy_acceptance', css_class='form-group'),
                css_class='form-row'
            ),
        )

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

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
