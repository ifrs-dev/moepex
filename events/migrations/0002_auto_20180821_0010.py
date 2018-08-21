# Generated by Django 2.1 on 2018-08-21 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='supervisor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='supervised_events', to=settings.AUTH_USER_MODEL, verbose_name='Orientador'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='supervisor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='supervised_experiments', to=settings.AUTH_USER_MODEL, verbose_name='Orientador'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(help_text='Paragráfo único com no máximo 100 palavras.', verbose_name='Resumo (Breve descrição, no máximo 100 palavras)'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='description',
            field=models.TextField(help_text='Resumo (Breve descrição, no máximo 100 palavras)', verbose_name='Resumo'),
        ),
    ]
