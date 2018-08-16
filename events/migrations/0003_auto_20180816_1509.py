# Generated by Django 2.0.6 on 2018-08-16 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20180816_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(help_text='Paragráfo único com no máximo 100 palavras.', verbose_name='Resumo'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='description',
            field=models.TextField(help_text='Paragráfo único com no máximo 50 palavras.', verbose_name='Resumo'),
        ),
    ]
