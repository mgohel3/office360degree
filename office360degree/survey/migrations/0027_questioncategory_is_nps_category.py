# Generated by Django 5.0.2 on 2024-02-28 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0026_submission_company_submission_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioncategory',
            name='is_nps_category',
            field=models.BooleanField(default=False),
        ),
    ]
