import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'CPF'
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean_username(self):
        cpf = self.cleaned_data['username']
        value = cpf
        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        orig_value = value[:]
        try:
            int(value)
        except ValueError:
            raise forms.ValidationError("CPF Inválido!")
        if len(value) != 11:
            raise forms.ValidationError("CPF Inválido!")
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise forms.ValidationError("CPF Inválido!")

        return cpf
