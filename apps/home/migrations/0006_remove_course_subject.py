# Generated by Django 3.2.6 on 2023-11-28 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_schedule_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='subject',
        ),
    ]
