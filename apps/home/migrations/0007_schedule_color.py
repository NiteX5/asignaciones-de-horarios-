# Generated by Django 3.2.6 on 2023-12-02 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_course_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='color',
            field=models.CharField(default='#0071c5', max_length=7),
        ),
    ]