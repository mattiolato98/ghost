from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('home', views.DashboardTemplateView.as_view(), name='home'),
    path('token_list', views.SignInTokenListView.as_view(), name='token-list'),
    path('generate_token', views.generate_token, name='generate-token'),
]
