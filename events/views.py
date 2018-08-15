from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect

from events.models import Event, Registration, Group, Experiment
from events.forms import EventForm, ExperimentForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm

class ExperimentCreateView(CreateView):
    model = Experiment
    template_name = 'experiments/experiment-create.html'
    form_class = ExperimentForm

class HomeView(ListView):
    model = Event
    template_name = 'event_site/index.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['experiments'] = Experiment.objects.filter(status=2)
        context['events'] = Event.objects.filter(status=2)
        return context

class EventListView(ListView):
    model = Event
    
    def get_context_data(self, *args, **kwargs):
        context['approved'] = Event.objects.filter(status=2)
        context['submited'] = Event.objects.filter(status=1)
        context['notapproved'] = Event.objects.filter(status=3)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['groups'] = Group.objects.filter(event=self.get_object())
        try:
            events = Registration.objects.filter(event=self.get_object(), user=user)
            if events.exists():
                context['registred'] = True
            else:
                context['registred'] = False
        except:
            context['not_user'] = True
        return context

class ExperimentDetailView(DetailView):
    model = Experiment
    template_name = 'experiments/experiment-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['groups'] = Group.objects.filter(experiment=self.get_object())
        try:
            experiment = Registration.objects.filter(experiment=self.get_object(), user=user)
            if events.exists():
                context['registred'] = True
            else:
                context['registred'] = False
        except:
            context['not_user'] = True
        return context



