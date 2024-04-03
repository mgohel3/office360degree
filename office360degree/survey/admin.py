from django.contrib import admin
from .models import Survey, Question, Submission, Answer, QuestionCategory, SurveyQuestion

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'creator', 'created_at']
    search_fields = ['title', 'creator__username']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'survey', 'category']
    search_fields = ['prompt', 'survey__title', 'category__name']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['survey', 'created_at', 'is_complete']
    search_fields = ['survey__title', 'is_complete']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['submission', 'rating' ]
    search_fields = ['submission__survey__title', 'option__text']

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'category']
    search_fields = ['question_text', 'category__name']