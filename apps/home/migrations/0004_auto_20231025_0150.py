# Generated by Django 3.2.6 on 2023-10-25 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_assignments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignments',
            name='course',
        ),
        migrations.AddField(
            model_name='assignments',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subjects'),
        ),
    ]
