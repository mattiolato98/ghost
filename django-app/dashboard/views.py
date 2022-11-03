import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from dashboard.decorators import manager_required
from dashboard.models import SignInToken


@method_decorator([login_required, manager_required], name='dispatch')
class DashboardTemplateView(TemplateView):
    template_name = 'dashboard/dashboard_home.html'


@method_decorator([login_required, manager_required], name='dispatch')
class SignInTokenListView(ListView):
    model = SignInToken
    template_name = 'dashboard/token_list.html'
    context_object_name = 'signin_tokens'


@login_required
@manager_required
def generate_token(request):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    SignInToken.objects.create(token=token)

    return HttpResponseRedirect(reverse_lazy('dashboard:token-list'))
