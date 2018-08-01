from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView

from events.models import Event, Registration
from events.forms import EventForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm


class EventListView(ListView):
    model = Event
    template_name = 'event_site/index.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-detail.html'



class EventInAvaliation(EventListView):
    queryset = Event.objects.filter(status=1)


class EventApproved(EventListView):
    queryset = Event.objects.filter(status=2)


class EventInCorrections(EventListView):
    queryset = Event.objects.filter(status=3)


class EventNoApproved(EventListView):
    queryset = Event.objects.filter(status=4)