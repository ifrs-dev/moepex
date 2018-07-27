from django.views.generic.edit import CreateView
from django.views.generic import View, ListView

from events.models import Event, Registration
from events.forms import EventForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm


class EventListView(ListView):
    model = Event
    template_name = 'event_site/index.html'
