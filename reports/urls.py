from django.urls import path, include
#from documents.views import *
from .views import *

urlpatterns = [
    path('', user_reports, name='user_reports'),
    path('create/', create_report, name='create_report'),
    path("<str:report_pk>/", view_report, name="view_report"),
    path("<str:report_pk>/share/", change_report_visibility, name="change_report_visibility"),
    path("<str:report_pk>/generate/", generate_report, name="generate_report"),
    path("public/<str:report_pk>/", public_reports, name="public_reports"),
    path("<str:report_pk>/delete/", delete_report, name="delete_report"),
    path("<str:report_pk>/documents/", include('documents.urls')),
]
