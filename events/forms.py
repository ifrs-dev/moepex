from django import forms

from events.models import Event, Experiment

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('status',)

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = ('status',)