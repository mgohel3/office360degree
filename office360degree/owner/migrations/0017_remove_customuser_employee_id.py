# Generated by Django 5.0.3 on 2024-03-14 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0016_alter_customuser_employee_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='employee_id',
        ),
    ]
