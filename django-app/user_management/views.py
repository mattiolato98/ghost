from django.shortcuts import render
from django.views.generic import TemplateView


class SettingsTemplateView(TemplateView):
    template_name = 'user_management/settings.html'
