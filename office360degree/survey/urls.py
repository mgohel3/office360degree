from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("survey-list/", views.survey_list, name="survey-list"),  # Update the path to survey_list
    path("<int:pk>/", views.detail, name="survey-detail"),  # Update the path to detail
    path("create/", views.create, name="survey-create"),  # Update the path to create
    path("<int:pk>/delete/", views.delete, name="survey-delete"),  # Update the path to delete
    path("<int:pk>/edit/", views.edit, name="survey-edit"),  # Update the path to edit
    path("<int:pk>/question/", views.question_create, name="survey-question-create"),  # Update the path to question_create
    path(
        "<int:survey_pk>/question/<int:question_pk>/option/",
        views.option_create,
        name="survey-option-create",
    ),
    path("<int:pk>/start/", views.start, name="survey-start"),  # Update the path to start
    path("<int:survey_pk>/submit/<int:sub_pk>/", views.submit, name="survey-submit"),  # Update the path to submit
    path("<int:pk>/thanks/", views.thanks, name="survey-thanks"),  # Update the path to thanks
    path("manage-categories/", views.manage_categories, name="manage-categories"),
    path("result/", views.result, name="result"),
    path('categories/', views.category_list, name='category_list'),

]
