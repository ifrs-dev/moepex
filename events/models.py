from django.db import models
from django.contrib.auth.models import User


CHOICES_STATUS_EVENT = (
    (1, "Submetido"),
    (2, "Aprovado"),
    (3, "Não aprovado"),
)

CHOICES_STATUS_REGISTRATION = (
    (1, "Inscrito"),
    (2, "Presente"),
    (3, "Ausente"),
)

CHOICES_WORKLOADS = (
    (1, '2 horas'),
    (2, '4 horas'),
)

CHOICES_SHIFTS = (
    (1, 'Manhã'),
    (1, 'Tarde'),
    (1, 'Noite'),
)


class Experiment(models.Model):

    class Meta:
        verbose_name = "Experimento"
        verbose_name_plural = "Experimentos"

    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Resumo', help_text='Paragráfo único com no máximo 50 palavras.')
    goal = models.TextField(verbose_name='Objetivo')
    status = models.IntegerField(choices=CHOICES_STATUS_EVENT, default=1, verbose_name='Status')
    authors = models.ManyToManyField(User, verbose_name='Autores', related_name='experiments')

    def __str__(self):
        return self.title
    def get_author(self):
        return ', '.join([u.get_full_name() for u in self.authors.all()])



class Event(models.Model):

    class Meta:
        verbose_name = 'Minicurso'
        verbose_name_plural = 'Minicursos'

    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Resumo', help_text='Paragráfo único com no máximo 100 palavras.')
    goal = models.TextField(verbose_name='Objetivo')
    public = models.CharField(max_length=200, verbose_name='Público Alvo')
    vacancies = models.PositiveIntegerField(verbose_name='Número Máximo de Participantes')
    requirements = models.TextField(verbose_name='Pré-requisitos', blank=True, null=True)
    materials = models.TextField(verbose_name='Material Necessário', blank=True, null=True)
    workload = models.PositiveIntegerField(verbose_name='Carga Horária', choices=CHOICES_WORKLOADS)
    authors = models.ManyToManyField(User, verbose_name='Autores', related_name='events')
    status = models.IntegerField(choices=CHOICES_STATUS_EVENT, default=1, verbose_name='Status')

    def __str__(self):
        return self.title

    def get_author(self):
        return ', '.join([u.get_full_name() for u in self.authors.all()])

class Group(models.Model):

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    shift = models.PositiveIntegerField(choices=CHOICES_SHIFTS, verbose_name='Turno')
    datetime = models.DateField(verbose_name='Data')
    local = models.CharField(max_length=100, verbose_name='Local')

    def __str__(self):
        return self.event.title + ' - Turma ' + str(self.id)


class Registration(models.Model):

    class Meta:
        unique_together = (('group', 'user'),)
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='registrations')
    status = models.IntegerField(choices=CHOICES_STATUS_REGISTRATION, default=1)

    def __str__(self):
        return self.group.event.title + ' - ' + self.user.first_name
