from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget

from events.models import Event, Experiment, Group
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('status', 'local',)
        widgets = {
            'supervisor': Select2Widget,
            'authors': Select2MultipleWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].choices = [(u.id, u.get_full_name()) for u in User.objects.all()]
        self.fields['supervisor'].choices = [(u.id, u.get_full_name()) for u in User.objects.filter(groups__name='servidores')]
        self.fields['supervisor'].choices += [('', '--------')]

class ExperimentForm(EventForm):
    class Meta:
        model = Experiment
        exclude = ('status',)
        widgets = {
            'supervisor': Select2Widget,
            'authors': Select2MultipleWidget,
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ()
