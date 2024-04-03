from django.db import models
from django.utils import timezone
from datetime import timedelta

class QuestionCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    is_nps_category = models.BooleanField(default=False) # NPS Category is used for NPS survey
    is_ees_category = models.BooleanField(default=False) # EES Category is used for EES survey

    def __str__(self):
        return f"{self.name} - {self.description}"

class Survey(models.Model):
    """A survey created by a user."""

    DURATION_CHOICES = [
        ("7", "7 days"),
        ("15", "15 days"),
        ("30", "30 days"),
    ]

    FREQUENCY_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("yearly", "Yearly"),
    ]

    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey('owner.CustomUser', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=timezone.now)
    questions = models.ManyToManyField('SurveyQuestion')
    company = models.ForeignKey('owner.Company', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default="7")  # Default to 7 days
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="weekly")  # Default to weekly

    def __str__(self):
        return self.title


class Question(models.Model):
    """A question in a survey"""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, default=None)
    prompt = models.CharField(max_length=128, default=None)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_nps_question = models.BooleanField(default=False)  # eNps Question
    is_ees_question = models.BooleanField(default=False)  # Employee Enagagement Survey Question

class Option(models.Model):
    """A multi-choice option or NPS indicator available as a part of a survey question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=128, default=None)
    is_nps_indicator = models.BooleanField(default=False)
    nps_value = models.IntegerField(default=0, choices=zip(range(0, 11), range(0, 11)))


class Submission(models.Model):
    """A set of answers to a survey's questions."""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey('owner.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey('owner.Company', on_delete=models.CASCADE, null=True, blank=True)

class Answer(models.Model):
    """An answer to a survey's questions."""

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=None)
    rating = models.IntegerField(default=0, choices=zip(range(0, 11), range(0, 11)))
    nps_score = models.IntegerField(default=-1, choices=zip(range(-1, 11), range(-1, 11)))  # New field

    def __str__(self):
        return f"Answer for Submission {self.submission.id}"


class SurveyQuestion(models.Model):
    """New model for admin-added survey questions."""
    question_text = models.CharField(max_length=255)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_nps_question = models.BooleanField(default=False)
    is_ees_question = models.BooleanField(default=False)
    user = models.ForeignKey('owner.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question_text
