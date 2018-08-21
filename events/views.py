from datetime import date

from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from events.models import Event, Registration, Group, Experiment
from events.forms import EventForm, ExperimentForm, GroupForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('group-list', args=(self.object.id,))

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial

class ExperimentCreateView(CreateView):
    model = Experiment
    template_name = 'events/event-create.html'
    form_class = ExperimentForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial


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
                events = Registration.objects.filter(group__event=self.get_object(), user=user)
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
        return redirect('event-detail', self.get_object().event.pk)


class MyRegistrationsListView(ListView):
    model = Registration
    template_name = 'events/my-events.html'


class GroupListView(DetailView):
    model = Event
    template_name = 'groups/group-list.html'


class GroupCreateView(DetailView, CreateView):
    model = Event
    template_name = 'groups/group-create.html'
    form_class = GroupForm

    def get_success_url(self):
        return reverse_lazy('group-list', args=(self.get_object().id,))

    def get(self, request, *args, **kwargs):
        if self.request.user == self.get_object().author:
            return super().get(request, *args, **kwargs)
        return redirect('event-detail', self.get_object().event.pk)

    def form_valid(self, form):
        form.instance.event = self.get_object()
        return super().form_valid(form)
