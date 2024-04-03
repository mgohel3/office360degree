from django.db import transaction
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from survey.models import Survey, Question, Answer, Submission, SurveyQuestion, QuestionCategory
from survey.forms import SurveyForm, QuestionForm, OptionForm, AnswerForm, BaseAnswerFormSet, SurveyQuestionForm
from net_promoter_score.models import UserScore
from net_promoter_score.forms import UserScoreForm

def landing(request):
    # Your view logic here
    return render(request, 'landing.html')  # Replace 'landing.html' with your actual template name
@login_required
def survey_list(request):
    survey = Survey.objects.filter(creator=request.user).order_by("-created_at").all()
    return render(request, "survey/list.html", {"survey": survey})

@login_required
def detail(request, pk):
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user, is_active=True
        )
    except Survey.DoesNotExist:
        raise Http404()

    questions = survey.question_set.all()

    for question in questions:
        total_answers = Answer.objects.filter(submission__survey=survey, submission__is_complete=True).count()
        for option in question.option_set.all():
            num_answers = Answer.objects.filter(nps_score=option.nps_score, submission__survey=survey,
                                                submission__is_complete=True).count()
            option.percent = 100.0 * num_answers / total_answers if total_answers else 0

    host = request.get_host()
    public_path = reverse("survey-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    num_submissions = survey.submission_set.filter(is_complete=True).count()

    return render(
        request,
        "survey/detail.html",
        {
            "survey": survey,
            "public_url": public_url,
            "questions": questions,
            "num_submissions": num_submissions,
        },
    )

@login_required
def create(request):
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.creator = request.user
            survey.save()
            # Assuming you have a many-to-many field for questions in SurveyQuestion model
            selected_question_ids = request.POST.getlist('selected_questions')
            selected_questions = SurveyQuestion.objects.filter(id__in=selected_question_ids)
            survey.questions.set(selected_questions)
            return redirect('owner:ac_survey_questions')
    else:
        form = SurveyForm()

    # Provide the list of available questions to the template
    questions = SurveyQuestion.objects.all()

    return render(request, "survey/create.html", {"form": form, "questions": questions})

@login_required
def delete(request, pk):
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        survey.delete()

    return redirect("survey-list")

@login_required
def edit(request, pk):
    try:
        survey = Survey.objects.prefetch_related("questions__option_set").get(
            pk=pk, creator=request.user, is_active=False
        )
    except Survey.DoesNotExist:
        raise Http404()

    # Fetch predefined questions associated with the survey
    predefined_questions = survey.questions.all()

    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey-detail", pk=pk)
    else:
        questions = survey.questions.all()
        return render(
            request,
            "survey/edit.html",
            {"survey": survey, "questions": questions, "predefined_questions": predefined_questions}
        )
@login_required
def question_create(request, pk):
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()

            # Redirect to the 'survey-question-create' URL with the survey's primary key
            return redirect("survey-question-create", pk=survey.pk)
    else:
        form = QuestionForm()

    return render(request, "survey/question.html", {"survey": survey, "form": form})

@login_required
def manage_categories(request):
    categories = QuestionCategory.objects.all()

    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect("manage-categories")
    else:
        category_form = CategoryForm()

    return render(request, "survey/manage_categories.html", {"categories": categories, "category_form": category_form})

@login_required
def option_create(request, survey_pk, question_pk):
    survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)

    if request.method == "POST":
        form = UserScoreForm(request.POST, user=request.user)
        if form.is_valid():
            score = form.save(commit=False)
            score.save()
    else:
        form = UserScoreForm()

    # Fetch existing Net Promoter Scores for the current question
    net_promoter_scores = UserScore.objects.filter(question=question, user=request.user)

    return render(
        request,
        "survey/options.html",
        {"survey": survey, "question": question, "scores": net_promoter_scores, "form": form},
    )

def start(request, pk):
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    if request.method == "POST":
        sub = Submission.objects.create(survey=survey)
        return redirect("survey-submit", survey_pk=pk, sub_pk=sub.pk)

    return render(request, "survey/start.html", {"survey": survey})

@login_required
def submit(request, survey_pk, sub_pk):
    try:
        survey = Survey.objects.get(pk=survey_pk, is_active=True)
    except Survey.DoesNotExist:
        raise Http404()

    try:
        sub = survey.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()

    # Use 'SurveyQuestion' model
    questions = SurveyQuestion.objects.filter(survey=survey)

    # Add NPS form for each question
    NPSFormSet = formset_factory(UserScoreForm, extra=len(questions))

    if request.method == "POST":
        nps_formset = NPSFormSet(request.POST, prefix='nps', form_kwargs={'user': request.user})

        if nps_formset.is_valid():
            with transaction.atomic():
                # Save NPS responses for each question
                for i, nps_form in enumerate(nps_formset):
                    question = get_object_or_404(SurveyQuestion, pk=questions[i].pk)
                    nps_score = nps_form.save(commit=False)
                    nps_score.submission = sub
                    nps_score.survey = survey
                    nps_score.question = question
                    nps_score.questioncategory = question.category
                    nps_score.is_nps_question = question.is_nps_question
                    nps_score.is_ees_question = question.is_ees_question
                    nps_score.save()

                sub.user = request.user
                sub.company = request.user.company
                sub.is_complete = True
                sub.save()

            return redirect("survey-thanks", pk=survey_pk)

    else:
        nps_formset = NPSFormSet(prefix='nps', form_kwargs={'user': request.user})

    question_forms = zip(questions, nps_formset)

    return render(
        request,
        "survey/submit.html",
        {"survey": survey, "question_forms": question_forms, "nps_formset": nps_formset},
    )

def thanks(request, pk):
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    return render(request, "survey/thanks.html", {"survey": survey})

def result(request):
    # Your view logic here
    return render(request, 'survey/result.html')

def category_list(request):
    categories = QuestionCategory.objects.all()
    return render(request, 'survey/category_list.html', {'categories': categories})