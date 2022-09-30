from django.urls import path
from django.contrib.auth import views as auth_views
from user_management import views


app_name = 'user_management'

urlpatterns = [
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('settings', views.SettingsTemplateView.as_view(), name='settings'),
]
