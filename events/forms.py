from django import forms

from events.models import Event, Experiment
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	self.fields['authors'].choices = [(u.id, u.get_full_name()) for u in User.objects.all()]

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = ('status',)