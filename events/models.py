from django.db import models
from django.contrib.auth.models import User
CHOICES_STATUS_EVENT = (
    (1, "Em avaliação"),
    (2, "Aprovado"),
    (3, "Necessita de correções"),
    (4, "Não aprovado"),
)

CHOICES_STATUS_REGISTRATION = (
    (1, "Inscrito"),
    (2, "Presente"),
    (3, "Ausente"),
)
CHOICES_ROLE = (
    (1, "Ouvinte"),
    (2, "Ministrante"),
)

class Event(models.Model):
    title = models.CharField(max_length=45, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')
    status = models.IntegerField(choices=CHOICES_STATUS_EVENT, default=1, verbose_name='Status')
    local = models.CharField(max_length=100, verbose_name='Local')
    bio_author = models.TextField(verbose_name='Descrição do Autor')
    start_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(verbose_name='Data Final')
    registration_date = models.DateField(verbose_name='Data de Registro')
    workload = models.CharField(verbose_name='Carga Horária', max_length=20)
    education = models.CharField(max_length=100, verbose_name='Formação')
    degree = models.CharField(max_length=100, verbose_name='Titulação', default='VII Moepex - Mostra Ensino, Pesquisa e Extensão ')
    vacancies = models.PositiveIntegerField(verbose_name='Vagas')
    
    def __str__(self):
        return self.title


class Registration(models.Model):

    class Meta:
        unique_together = (('event', 'user'),)

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.IntegerField(choices=CHOICES_STATUS_REGISTRATION, default=1)
    role = models.IntegerField(choices=CHOICES_ROLE, default=1)

    def __str__(self):
        return self.event.title + ' - ' + self.user.first_name
