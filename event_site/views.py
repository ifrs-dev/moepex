from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from event_site.forms import SignUpForm
from events.models import Event, Experiment


class HomeView(ListView):
    model = Event
    template_name = 'event_site/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['experiments'] = Experiment.objects.filter(status=2)
        context['events'] = Event.objects.filter(status=2)
        context['users'] = User.objects.all()
        return context


class PresentationTemplateView(TemplateView):
    template_name = 'event_site/presentation.html'


class SignUpView (CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
