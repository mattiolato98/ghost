from django.urls import path
from transcribe import views

app_name = 'transcribe'

urlpatterns = [
    path('form', views.TranscriptionCreateView.as_view(), name='transcription-form'),
    path('list', views.TranscriptionListView.as_view(), name='transcription-list'),
    path('list/<int:pk>', views.TranscriptionListView.as_view(), name='transcription-list'),
]
