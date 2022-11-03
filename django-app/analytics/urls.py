from django.urls import path
from analytics import views

app_name = 'analytics'

urlpatterns = [
    path('stats', views.StatsView.as_view(), name='stats'),
]
