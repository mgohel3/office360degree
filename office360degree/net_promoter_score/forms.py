from typing import Any
from django import forms
from .models import UserScore
from survey.models import SurveyQuestion

class UserScoreForm(forms.ModelForm):
    """Form for capturing NPS score."""

    reason = forms.CharField(max_length=512, required=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "user" not in kwargs:
            raise ValueError("Score must have a valid user.")
        self.user = kwargs.pop("user")
        super(UserScoreForm, self).__init__(*args, **kwargs)

        # Update queryset to filter questions based on user
        self.fields['question'].queryset = SurveyQuestion.objects.filter(user=self.user)

    class Meta:
        model = UserScore
        fields = ("question", "score", "reason")
        exclude = ("user",)

        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.TextInput(attrs={'type': 'range', 'class': 'form-range', 'min': '0', 'max': '10', 'list': 'score-options'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }

        datalists = {
            'score': [
                (value, value) for value in range(11)  # Assuming range from 0 to 10
            ]
        }

    def clean_score(self) -> int:
        score = self.cleaned_data["score"]  # type: int
        if score < 0 or score > 10:
            raise forms.ValidationError("Score must be between 0-10")
        return score

    def save(self, commit: bool = True) -> UserScore:
        """Set the user attr of the score."""
        score = super(UserScoreForm, self).save(commit=False)
        score.user = self.user
        return score.save()