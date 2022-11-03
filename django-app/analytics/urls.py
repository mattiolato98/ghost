from django.urls import path
from analytics import views

app_name = 'analytics'

urlpatterns = [
    path('stats', views.StatsTemplateView.as_view(), name='stats'),
]
