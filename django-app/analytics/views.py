import datetime as dt
import pytz

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from analytics.models import Stats
from dashboard.decorators import manager_required


@method_decorator([login_required, manager_required], name='dispatch')
class StatsTemplateView(TemplateView):
    template_name = 'analytics/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsTemplateView, self).get_context_data(**kwargs)

        context['users'] = get_user_model().objects.count()
        context['unsubscribed_users'] = Stats.objects.first().unsubscribed_users
        context['subscribers_last_7_days'] = len(get_user_model().objects.filter(
            date_joined__gte=dt.datetime.now(pytz.timezone('Europe/Rome')) - dt.timedelta(days=7)
        ))
        context['percent_increment_subscribers_last_7_days'] = ((
            context['subscribers_last_7_days']
        ) / (context['users'] - context['subscribers_last_7_days'])) * 100
        context['logged_in_last_7_days'] = get_user_model().objects.filter(
            last_login__gte=dt.datetime.now(pytz.timezone('Europe/Rome')) - dt.timedelta(days=7)
        ).count()
        context['percent_logged_in_last_7_days'] = (
            context['logged_in_last_7_days'] / context['users']
        ) * 100
        context['inactive_users'] = get_user_model().objects.filter(is_active=False).count()

        return context
