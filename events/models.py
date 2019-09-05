from django.db import models
from django.contrib.auth.models import User

def get_name(self):
    return self.get_full_name()

User.add_to_class("__str__", get_name)

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

CHOICES_SHIFTS_4 = (
    (1, '04/10/2018 - 13:15 às 16:50'),
    (2, '04/10/2018 - 19:00 às 22:30'),
)

CHOICES_SHIFTS_2 = (
    (11, '04/10/2018 - 13:15 às 14:55'),
    (12, '04/10/2018 - 15:10 às 16:50'),
    (13, '04/10/2018 - 19:00 às 20:40'),
    (14, '04/10/2018 - 20:50 às 22:30'),
    (15, '04/10/2018 - 17:00 às 19:00'),
)

CHOICES_SHIFTS = CHOICES_SHIFTS_2 + CHOICES_SHIFTS_4


class Event(models.Model):

    class Meta:
        verbose_name = 'Minicurso'
        verbose_name_plural = 'Minicursos'

    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Resumo (Breve descrição)', help_text='Paragráfo único com no máximo 100 palavras.')
    goal = models.TextField(verbose_name='Objetivo')
    public = models.CharField(max_length=200, verbose_name='Público Alvo')
    vacancies = models.PositiveIntegerField(verbose_name='Número Máximo de Participantes')
    requirements = models.TextField(verbose_name='Pré-requisitos', blank=True, null=True)
    materials = models.TextField(verbose_name='Recursos necessários', blank=True, null=True)
    workload = models.PositiveIntegerField(verbose_name='Carga Horária', choices=CHOICES_WORKLOADS)
    status = models.IntegerField(choices=CHOICES_STATUS_EVENT, default=1, verbose_name='Status')
    author = models.ForeignKey(User, verbose_name='Autor', on_delete=models.PROTECT, related_name='author_events')
    co_authors = models.ManyToManyField(User, verbose_name='Co-autores', related_name='co_authors_events', blank=True)
    supervisor = models.ForeignKey(User, verbose_name='Orientador', on_delete=models.PROTECT, related_name='supervised_events', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_author(self):
        authors = [u.get_full_name() for u in self.co_authors.all()]
        authors += [self.author.get_full_name()]
        if self.supervisor:
            authors += [self.supervisor.get_full_name()]
        return ', '.join(authors)


class Group(models.Model):

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        unique_together = ['event', 'shift']

    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='groups')
    shift = models.PositiveIntegerField(choices=CHOICES_SHIFTS, verbose_name='Data')
    local = models.CharField(max_length=100, verbose_name='Local', null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.event.title, self.get_shift_display())


class Registration(models.Model):

    class Meta:
        unique_together = (('group', 'user'),)
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='registrations')
    status = models.IntegerField(choices=CHOICES_STATUS_REGISTRATION, default=1)

    def __str__(self):
        return self.group.event.title + ' - ' + self.user.first_name
