# Generated by Django 5.0.2 on 2024-02-09 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_survey_unique_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='unique_link',
        ),
    ]
