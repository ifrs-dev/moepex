from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect

from events.models import Event, Registration, Group
from events.forms import EventForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm


class HomeView(ListView):
    model = Event
    template_name = 'event_site/index.html'


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

