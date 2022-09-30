from django.urls import path
from transcribe import views

app_name = 'transcribe'

urlpatterns = [
    path('', views.TranscriptionCreateView.as_view(), name='transcribe'),
]
