from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from user_management.decorators import not_authenticated_only


@method_decorator(not_authenticated_only, name='dispatch')
class HomeTemplateView(TemplateView):
    template_name = 'home.html'
