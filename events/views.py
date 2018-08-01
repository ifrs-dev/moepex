from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView

from events.models import Event, Registration
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


class EventListView(EventListView):
    model = Event
    template_name = 'event_site/event-list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['inavaliation'] = Event.objects.filter(status=1)
        context['approved'] = Event.objects.filter(status=2)
        context['incorrections'] = Event.objects.filter(status=2)
        context['notapproved'] = Event.objects.filter(status=2)
        return context
