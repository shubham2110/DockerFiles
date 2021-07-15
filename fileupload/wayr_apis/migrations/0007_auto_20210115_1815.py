# Generated by Django 3.0.7 on 2021-01-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayr_apis', '0006_auto_20210115_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trips',
            name='date',
        ),
        migrations.RemoveField(
            model_name='trips',
            name='time',
        ),
        migrations.AddField(
            model_name='trips',
            name='datetime',
            field=models.CharField(default='202101151815', max_length=15, verbose_name='trip date time'),
        ),
    ]