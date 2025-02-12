# Generated by Django 5.0.2 on 2024-02-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0009_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, help_text='Max size: 320 x 320 px, Max file size: 750KB', max_length=255, null=True, upload_to='owner/static/assets/img/avatars/'),
        ),
    ]
