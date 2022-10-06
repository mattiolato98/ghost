from django.urls import path
from django.contrib.auth import views as auth_views
from user_management import views


app_name = 'user_management'

urlpatterns = [
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('delete', views.UserDeleteView.as_view(), name='delete'),
    path('verify/<str:user_id_b64>/<str:user_token>', views.verify_user_email, name='verify-user-email'),
    path('email/verification_needed', views.EmailVerificationNeededView.as_view(), name='email-verification-needed'),
    path('email/verified', views.EmailVerifiedView.as_view(), name='email-verified'),
    path('settings', views.SettingsTemplateView.as_view(), name='settings'),
    path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('cookie-policy', views.CookiePolicyView.as_view(), name='cookie-policy'),
    path('ajax-check-username-exists', views.ajax_check_username_exists, name='ajax-check-username-exists'),
]
