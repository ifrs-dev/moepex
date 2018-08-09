# Generated by Django 2.1 on 2018-08-09 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Resumo')),
                ('goal', models.TextField(verbose_name='Objetivo')),
                ('public', models.CharField(max_length=200, verbose_name='Público Alvo')),
                ('vacancies', models.PositiveIntegerField(verbose_name='Número Máximo de Participantes')),
                ('requirements', models.TextField(blank=True, null=True, verbose_name='Pré-requisitos')),
                ('materials', models.TextField(blank=True, null=True, verbose_name='Material Necessário')),
                ('workload', models.PositiveIntegerField(choices=[(1, '2 horas'), (2, '4 horas')], verbose_name='Carga Horária')),
                ('status', models.IntegerField(choices=[(1, 'Submetido'), (2, 'Aprovado'), (3, 'Não aprovado')], default=1, verbose_name='Status')),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Autores')),
            ],
            options={
                'verbose_name': 'Minicurso',
                'verbose_name_plural': 'Minicursos',
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Resumo')),
                ('goal', models.TextField(verbose_name='Objetivo')),
                ('status', models.IntegerField(choices=[(1, 'Submetido'), (2, 'Aprovado'), (3, 'Não aprovado')], default=1, verbose_name='Status')),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Autores')),
            ],
            options={
                'verbose_name': 'Experimento',
                'verbose_name_plural': 'Experimentos',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.PositiveIntegerField(choices=[(1, 'Manhã'), (1, 'Tarde'), (1, 'Noite')], verbose_name='Turno')),
                ('date', models.DateField(verbose_name='Data')),
                ('local', models.CharField(max_length=100, verbose_name='Local')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Event')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Inscrito'), (2, 'Presente'), (3, 'Ausente')], default=1)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Inscrição',
                'verbose_name_plural': 'Inscrições',
            },
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together={('group', 'user')},
        ),
    ]
