from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.views.decorators.http import require_http_methods  # Add this import

from .forms import UserScoreForm
from .models import UserScore
from owner.models import CustomUser

def index(request):
    return render(request, 'net_promoter_score/index.html')

@require_http_methods(["POST", "GET"])
@user_passes_test(lambda u: u.is_authenticated)
def post_score(request: HttpRequest) -> JsonResponse:
    """
    POST/GET handler for NPS scores.

    Returns a JSON object, which includes a 'success' key that is True/False.
    If success is True, the response will also contain a 'score' value that
    is the UserScore.json() object.

        {
          "success": True,
          "score": {"id": 1, "user": 1, "score": 0, "group": "detractor"}
        }

    If success is False, the response will contain an 'errors' list:

        {
          "success": False,
          "errors": [["score", "Score must be between 0-10"]]
        }

    """
    if request.method == "POST":
        form = UserScoreForm(request.POST, user=request.user)
        if form.is_valid():
            score = form.save()
            return JsonResponse(
                {"success": True, "score": score.json()}, status=201
            )
        else:
            errors = [(k, v[0]) for k, v in list(form.errors.items())]
            return JsonResponse({"success": False, "errors": errors}, status=422)
    else:
        # Handle GET requests (if needed)
        return render(request, 'net_promoter_score/post_score.html', {'success': False, 'errors': []})

def nps_submissions(request):
    # Fetch NPS submissions, you might want to filter or order them based on your requirements
    nps_submissions = UserScore.objects.all()

    context = {'nps_submissions': nps_submissions}
    return render(request, 'net_promoter_score/nps_submissions.html', context)

def nps_summary(request):
    # Get the counts of promoters, detractors, and neutrals
    promoters_count = UserScore.objects.promoters().count()
    detractors_count = UserScore.objects.detractors().count()
    neutrals_count = UserScore.objects.neutrals().count()

    context = {
        'promoters_count': promoters_count,
        'detractors_count': detractors_count,
        'neutrals_count': neutrals_count,
    }

    return render(request, 'net_promoter_score/nps_summary.html', context)

def ees_user_scores(request):
    users = CustomUser.objects.all()
    overall_scores = []

    for user in users:
        user_scores = UserScore.objects.filter(user=user, is_ees_question=True)
        total_score = sum([score.score for score in user_scores])
        average_score = total_score / len(user_scores) if len(user_scores) > 0 else 0
        overall_scores.append({'user': user, 'overall_score': average_score})

    return render(request, 'net_promoter_score/ees_user_scores.html', {'overall_scores': overall_scores})

def thanks_page(request):
    return render(request, 'survey/thanks_page.html')
