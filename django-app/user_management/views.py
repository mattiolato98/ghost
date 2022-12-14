from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from analytics.models import Stats
from dashboard.models import SignInToken
from user_management.decorators import not_authenticated_only
from user_management.forms import LoginForm, PlatformUserCreationForm, UpdatePasswordForm
from user_management.models import PlatformUser


account_activation_token = PasswordResetTokenGenerator()


@method_decorator(not_authenticated_only, name='dispatch')
class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


@method_decorator(not_authenticated_only, name='dispatch')
class RegistrationView(CreateView):
    form_class = PlatformUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('user_management:email-verification-needed')

    def form_valid(self, form):
        try:
            token = SignInToken.objects.get(
                token=form.cleaned_data['token'],
                is_active=True,
            )
        except SignInToken.DoesNotExist:
            form.add_error('token', error=_('Invalid token.'))
            return self.form_invalid(form)

        token.is_active = False
        token.save()

        self.object = form.save(commit=False)

        response = super(RegistrationView, self).form_valid(form)

        mail_subject = 'Conferma la tua email | Soulscribe'
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
                     + '''Ti diamo il benvenuto in Soulscribe!\n'''
                     + '''\nConferma la tua email:'''
                     + f'''\n{self.request.build_absolute_uri(relative_confirm_url)}\n'''
                     + '''\nA presto, \nSoulscribe Team''')
        )

        self.object.token_sent = True
        self.object.is_active = False
        self.object.save()

        return response


class UpdatePasswordView(LoginRequiredMixin, UpdateView):
    """
    Password UpdateView.
    """
    model = get_user_model()
    template_name = 'user_management/password_update.html'
    success_url = reverse_lazy('user_management:settings')
    form_class = UpdatePasswordForm

    def get_object(self, queryset=None):
        """Avoid passing users' primary keys in the URL"""
        return self.request.user

    def form_valid(self, form):
        """Checks that the old password matches"""
        if self.request.user.check_password(form.cleaned_data['old_password']):
            return super(UpdatePasswordView, self).form_valid(form)
        else:
            form.add_error('old_password', error=_('The old password is not correct'))
            return self.form_invalid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "user_management/user_delete.html"
    success_url = reverse_lazy("home")
    model = get_user_model()

    def get_object(self, queryset=None):
        """Avoid passing users' primary keys in the URL"""
        return self.request.user

    def post(self, request, *args, **kwargs):
        stats = Stats.objects.first()
        stats.unsubscribed_users += 1
        stats.save()
        return super(UserDeleteView, self).post(request, *args, **kwargs)


class EmailVerificationNeededView(TemplateView):
    template_name = 'user_management/email_verification_needed.html'


class EmailVerifiedView(TemplateView):
    template_name = 'user_management/email_verified.html'


class SettingsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/settings.html'


@method_decorator(not_authenticated_only, name='dispatch')
class TokenRequestTemplateView(TemplateView):
    template_name = 'user_management/token_request.html'


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


@login_required
@require_GET
@csrf_protect
def ajax_check_username_is_correct(request):
    """Check if the username given by a user is correct in order to
    make them able to delete their account."""

    if request.GET.get('username') == request.user.username:
        return JsonResponse({'is_correct': True})
    return JsonResponse({'is_correct': False})