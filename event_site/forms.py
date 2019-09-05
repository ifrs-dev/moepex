import csv

from django import forms
from django.contrib.auth.models import User, Group



def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Apenas arquivos csv são aceitos.")

class ImportForm(forms.Form):
    docfile = forms.FileField(label='Selecionar Arquivo',validators=[validate_file_extension])


class ImportFormSIGAA(ImportForm):

    def clean_docfile(self):
        csv_file = self.cleaned_data['docfile']
        lines = csv_file.read().decode("utf-8").split("\n")
        for line in lines[1:]:
            fields = line.split(",")
            if len(fields) >= 3:
                username = fields[2].replace('"', '')
                name = fields[0].replace('"', '').strip().upper().split()
                first_name = name[0]
                last_name = ' '.join(name[1:])
                password = fields[4].replace('"', '')
                user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name)
                if created:
                    user.set_password(password)
                    user.save()
            else:
                break
        return csv_file


class ImportFormSIA(ImportForm):

    def clean_docfile(self):
        csv_file = self.cleaned_data['docfile']
        lines = csv_file.read().decode("utf-8").split("\n")
        for line in lines[1:]:
            fields = line.split(",")
            if len(fields) >= 3:
                cpf = fields[7].replace('"', '')
                username = '%s.%s.%s-%s' % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])
                name = fields[1].replace('"', '').strip().upper().split()
                first_name = name[0]
                last_name = ' '.join(name[1:])
                password = fields[0].replace('"', '')
                password = password
                user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name)
                if created:
                    user.set_password(password)
                    user.save()
            else:
                break
        return csv_file


class ImportFormServ(ImportForm):

    def clean_docfile(self):
        csv_file = self.cleaned_data['docfile']
        lines = csv_file.read().decode("utf-8").split("\n")
        serv_group, created = Group.objects.get_or_create(name='servidores')
        for line in lines[1:]:
            fields = line.split(",")
            if len(fields) >= 3:
                username = fields[2].replace('"', '').strip()
                name = fields[1].replace('"', '').strip().upper().split()
                first_name = name[0]
                last_name = ' '.join(name[1:])
                password = fields[0].replace('"', '').strip()
                try:
                    user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name)
                    serv_group.user_set.add(user)
                    if created:
                        user.set_password(password)
                        user.save()
                except:
                    pass
            else:
                break
        return csv_file
