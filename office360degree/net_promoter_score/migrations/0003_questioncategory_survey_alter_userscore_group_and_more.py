# Generated by Django 5.0.2 on 2024-02-09 10:18

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_promoter_score', '0002_promoterscore_source'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='userscore',
            name='group',
            field=models.CharField(choices=[('unknown', 'No answer'), ('detractor', 'Detractor (0-6)'), ('neutral', 'Neutral (7-8)'), ('promoter', 'Promoter (9-10)')], db_index=True, default='unknown', help_text='Detractor, neutral, or promoter.', max_length=10),
        ),
        migrations.AlterField(
            model_name='userscore',
            name='score',
            field=models.IntegerField(db_index=True, default=-1, help_text='0-6=Detractor; 7-8=Neutral; 9-10=Promoter', validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='userscore',
            name='source',
            field=models.CharField(blank=True, help_text="Source of user score, used for filtering results, e.g., 'app', 'web', 'email'.", max_length=20),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='net_promoter_score.questioncategory')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('draft', 'Draft')], default='draft', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='net_promoter_score.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_responses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='net_promoter_score.question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='net_promoter_score.surveyresponse')),
            ],
        ),
    ]
