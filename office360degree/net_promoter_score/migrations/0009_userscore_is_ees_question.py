# Generated by Django 5.0.2 on 2024-02-29 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_promoter_score', '0008_userscore_is_nps_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='userscore',
            name='is_ees_question',
            field=models.BooleanField(default=False),
        ),
    ]
