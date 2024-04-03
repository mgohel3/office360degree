# owner/urls.py
from django.urls import path
from .models import SBU
from .views import SignUpView, home, login_view, logout_view, dashboard_view, add_user, survey_view, survey_ees_view, survey_os_view, survey_es_view, survey_cs_view, reports_view, comments_view, team_view, usermanagement_view, account_settings_view, ac_survey_questions_view, puls_survey_frequency_view, custom_survey_launch_view, notifications_view, app_integration_view, profile_view, bulk_user_upload


app_name = 'owner'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('home/', home, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('survey/', survey_view, name='survey'),
    path('survey-ees/', survey_ees_view, name='survey_ees'),
    path('survey-os/', survey_os_view, name='survey_os'),
    path('survey-es/', survey_es_view, name='survey_es'),
    path('survey-cs/', survey_cs_view, name='survey_cs'),
    path('reports/', reports_view, name='reports'),
    path('comments/', comments_view, name='comments'),
    path('team/', team_view, name='team'),
    path('user-management/', usermanagement_view, name='usermanagement'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_user/', add_user, name='add_user'),
    path('bulk_user_upload/', bulk_user_upload, name='bulk_user_upload'),
    path('account_settings/', account_settings_view, name='account_settings'),
    path('ac_survey_questions/', ac_survey_questions_view, name='ac_survey_questions'),
    path('puls_survey_frequency/', puls_survey_frequency_view, name='puls_survey_frequency'),
    path('custom_survey_launch/', custom_survey_launch_view, name='custom_survey_launch'),
    path('notifications/', notifications_view, name='notifications'),
    path('app_integration/', app_integration_view, name='app_integration'),
    path('profile/', profile_view, name='profile'),

]
