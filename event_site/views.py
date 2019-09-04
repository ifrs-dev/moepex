import csv

from django.views.generic import TemplateView, FormView
from django.shortcuts import reverse
from django.http import HttpResponse

from event_site.forms import ImportFormSIGAA, ImportFormSIA, ImportFormServ
from events.models import Event

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = event.objects.all()
        return context


class SiaImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportFormSIA

    def get_success_url(self):
        return reverse('home')


class SigaaImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportFormSIGAA

    def get_success_url(self):
        return reverse('home')


class ServImporterView(FormView):
    template_name = 'importer.html'
    form_class = ImportFormServ

    def get_success_url(self):
        return reverse('home')

def build_row(user, event, role='Ouvinte'):
    row = ['', '', '', role, 'Mostra de minicursos', '', '28 de agosto de 2019', '']
    row[0] = user.get_full_name()
    row[1] = user.username
    row[2] = user.email
    row[5] = event.title
    row[7] = 'totalizando 8 horas'
    return row

def get_certified(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="certificados.csv"'
    writer = csv.writer(response)
    writer.writerow(['NOME_PARTICIPANTE','CPF_PARTICIPANTE','EMAIL_PARTICIPANTE','CONDICAO_PARTICIPACAO','FORMA_ACAO','TITULO_ACAO','PERIODO_REALIZACAO','CARGA_HORARIA'])

    events = event.objects.filter(status=2)

    for event in events:
        writer.writerow(build_row(event.author, event, 'autor(a)'))
        if event.supervisor:
            writer.writerow(build_row(event.supervisor, event, 'orientador(a)'))
        for coautor in event.co_authors.all():
            writer.writerow(build_row(coautor, event, 'co-autor(a)'))
    return response