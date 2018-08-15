from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from events.models import Event, Registration, Group, Experiment
from events.forms import EventForm, ExperimentForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm
    success_url = reverse_lazy('home')

class ExperimentCreateView(CreateView):
    model = Experiment
    template_name = 'experiments/experiment-create.html'
    form_class = ExperimentForm
    success_url = reverse_lazy('home')

class HomeView(ListView):
    model = Event
    template_name = 'event_site/index.html'

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
        context['not_user'] = False
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



class EventRegistrationView(DetailView):
    model = Event

    def get(self, request, *args, **kwargs):
        Registration.objects.create(event=self.get_object(), user=request.user)
        return redirect('my-events')

class MyRegistrationsListView(ListView):
    model = Registration
    template_name = 'events/my_events.html'

    def get_queryset(self):
        objects = Registration.objects.filter(user=self.request.user)
        return objects.order_by('event__start_date')


