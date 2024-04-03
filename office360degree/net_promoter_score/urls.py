# net_promoter_score/urls.py

from django.urls import path
from .views import post_score, nps_submissions, nps_summary, ees_user_scores

app_name = "net_promoter_score"

urlpatterns = [
    path('score/', post_score, name='post_score'),
    path('nps_submissions/', nps_submissions, name='nps_submissions'),
    path('nps_summary/', nps_summary, name='nps_summary'),
    path('ees_user_scores/', ees_user_scores, name='ees_user_scores'),
]
