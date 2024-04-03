from django import forms

from survey.models import Survey, Question, QuestionCategory, Option, SurveyQuestion
from django.utils import timezone
from net_promoter_score.forms import UserScoreForm
from owner.models import Company
from datetime import datetime
import random


class SurveyForm(forms.ModelForm):
    # Add a field for choosing questions
    selected_questions = forms.ModelMultipleChoiceField(
        queryset=SurveyQuestion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Select Questions',
    )

    class Meta:
        model = Survey
        fields = ["title", "company", "frequency", "date", "time", "duration"]

    widgets = {
        'company': forms.HiddenInput(),
    }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['readonly'] = True  # Make the title field read-only

        # Set the input format for the date field
        self.fields['date'].input_formats = ['%Y-%m-%d']

        # Set the input format for the time field
        self.fields['time'].input_formats = ['%H:%M:%S']

        if 'company' in self.fields and user and not self.instance.company:
            self.fields['company'].queryset = Company.objects.filter(id=user.company.id)
            self.initial['company'] = user.company.id

        # Set default value for the title field
        if not self.instance.title and user:
            company_name = user.company.name if user.company else "default-company"  # Replace with a default value if user.company is None
            survey_name = "puls_survey"
            creation_date = timezone.now().strftime("%d-%m-%Y")
            # Get the count of surveys created on the same date
            count_same_date_surveys = Survey.objects.filter(
                creator=user,
                date=timezone.now().date(),
            ).count()
            default_title = f"{company_name}-{survey_name}-{creation_date}-{count_same_date_surveys + 1}"
            self.initial['title'] = default_title

    def clean_time(self):
        # Ensure the time is stored in the user's timezone
        user_timezone = timezone.get_current_timezone()
        cleaned_time = self.cleaned_data['time']
        return timezone.make_aware(cleaned_time, user_timezone)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_active = True
        if commit:
            instance.save()
        return instance

class SurveyQuestionForm(forms.ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = ['question_text', 'category', 'is_nps_question', 'user']

    def __init__(self, *args, **kwargs):
        super(SurveyQuestionForm, self).__init__(*args, **kwargs)

class QuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=QuestionCategory.objects.all(), required=False)

    class Meta:
        model = Question
        fields = ["prompt", "category"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = QuestionCategory
        fields = ["name"]

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]

class AnswerForm(forms.Form):
    option = forms.ChoiceField(widget=forms.RadioSelect, required=True)

    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options", None)
        super().__init__(*args, **kwargs)
        if options:
            self.fields['option'].choices = [(str(option.pk), option.text) for option in options]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
