from django.urls import path
from transcribe import views

app_name = 'analytics_management'

urlpatterns = [
    path('', views.TranscribeView.as_view(), name='transcribe'),
]
