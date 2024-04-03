# Generated by Django 5.0.2 on 2024-02-29 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0027_questioncategory_is_nps_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_ees_question',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='is_ees_category',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='is_ees_question',
            field=models.BooleanField(default=False),
        ),
    ]
