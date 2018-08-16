from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from events.models import Event, Registration, Group, Experiment
from events.forms import EventForm, ExperimentForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['authors'] = self.request.user.pk
        return initial

class ExperimentCreateView(CreateView):
    model = Experiment
    template_name = 'events/event-create.html'
    form_class = ExperimentForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['authors'] = self.request.user.pk
        return initial

class HomeView(ListView):
    model = Event
    template_name = 'event_site/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['experiments'] = Experiment.objects.filter(status=2)
        context['events'] = Event.objects.filter(status=2)
        context['users'] = User.objects.all()
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['groups'] = Group.objects.filter(event=self.get_object())

        if not user.is_authenticated:
            context['registred'] = 'not_user'
        else:
            try:
                events = Registration.objects.filter(event=self.get_object(), user=user)
                if events.exists():
                    context['registred'] = 'valid'
            except:
                pass
        return context


class ExperimentDetailView(DetailView):
    model = Experiment
    template_name = 'experiments/experiment-detail.html'


class EventRegistrationView(DetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        Registration.objects.create(group=self.get_object(), user=request.user)
        return redirect('my-events')


class MyRegistrationsListView(ListView):
    model = Registration
    template_name = 'events/my-events.html'

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['events'] = Event.objects.filter(authors__icontains=self.request.user)
        context['experiments'] = Experiment.objects.filter(authors__icontains=self.request.user)
        return context
