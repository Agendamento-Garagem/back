# Generated by Django 4.1.1 on 2022-09-19 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0004_event_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='adm',
            field=models.CharField(default='', max_length=200),
        ),
    ]
