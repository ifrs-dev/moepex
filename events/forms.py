from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget

from events.models import Event, Group
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('status', 'local')
        widgets = {
            'supervisor': Select2Widget,
            'co_authors': Select2MultipleWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.filter(is_superuser=False)
        self.fields['co_authors'].choices = [(u.id, u.get_full_name()) for u in users]
        self.fields['supervisor'].choices = [(u.id, u.get_full_name()) for u in users.filter(groups__name='servidores')]
        self.fields['supervisor'].choices += [('', '--------')]



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('event', 'local', 'hour')
        widgets = {
            'datetime': forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', None)
        super().__init__(*args, **kwargs)
        self.fields['shift'].choices = self.choices
