from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, CreateView

from user_management.decorators import not_authenticated_only
from user_management.forms import LoginForm, PlatformUserCreationForm
from user_management.models import PlatformUser


account_activation_token = PasswordResetTokenGenerator()


@method_decorator(not_authenticated_only, name='dispatch')
class RegistrationView(CreateView):
    form_class = PlatformUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('user_management:email-verification-needed')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        response = super(RegistrationView, self).form_valid(form)

        mail_subject = 'Conferma la tua email | Ghost'
        relative_confirm_url = reverse(
            'user_management:verify-user-email',
            args=[
                urlsafe_base64_encode(force_bytes(self.object.pk)),
                account_activation_token.make_token(self.object)
            ]
        )

        self.object.email_user(
            subject=mail_subject,
            message=(f'''Ciao {self.object.username}\n'''
                     + '''Ti diamo il benvenuto in Ghost!\n'''
                     + '''\nConferma la tua email:'''
                     + f'''\n{self.request.build_absolute_uri(relative_confirm_url)}\n'''
                     + '''\nA presto, \nGhost Team''')
        )

        self.object.token_sent = True
        self.object.is_active = False
        self.object.save()

        return response


class EmailVerificationNeededView(TemplateView):
    template_name = 'user_management/email_verification_needed.html'


class EmailVerifiedView(TemplateView):
    template_name = 'user_management/email_verified.html'


class SettingsTemplateView(TemplateView):
    template_name = 'user_management/settings.html'


class PrivacyPolicyView(TemplateView):
    template_name = "user_management/privacy_policy.html"


class CookiePolicyView(TemplateView):
    template_name = "user_management/cookie-policy.html"


def ajax_check_username_exists(request):
    return (
        JsonResponse({'exists': True})
        if get_user_model().objects.filter(
            username=request.GET.get('username')
        ).exists()
        else JsonResponse({'exists': False}))


def user_login_by_token(request, user_id_b64=None, user_token=None):
    """
    Check the token is equal to one of user trying to verify its email.
    """
    try:
        uid = force_str(urlsafe_base64_decode(user_id_b64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, user_token):
        user.is_active = True
        user.save()
        login(request, user)
        return True

    return False


def verify_user_email(request, user_id_b64=None, user_token=None):
    """
    Check for the token and redirect to email verification succeeded page.
    """
    if not user_login_by_token(request, user_id_b64, user_token):
        message = _(f'Error. Attempt to validate email for the user {user_id_b64} with token {user_token}')
        subject = _('Authentication error')
        # in this case manager and admin are the same entity
        manager = PlatformUser.objects.get(is_manager=True)
        manager.email_user(subject=subject, message=message)
        # TODO: maybe provide an error message?
        return redirect('user_management:registration')

    return redirect('user_management:email-verified')
