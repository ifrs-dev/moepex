# Generated by Django 2.0.6 on 2018-08-31 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20180827_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='shift',
            field=models.PositiveIntegerField(choices=[(11, '04/10/2018 Tarde 1'), (12, '04/10/2018 Tarde 2'), (13, '04/10/2018 Noite 1'), (14, '04/10/2018 Noite 2'), (1, '04/10/2018 Tarde'), (2, '04/10/2018 Noite')], verbose_name='Data'),
        ),
    ]
