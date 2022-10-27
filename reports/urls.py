from django.urls import path
from .views import *

urlpatterns = [
    path('', user_reports, name='user_reports'),
    path("<str:pk>/", generated_report, name="generated_report"),
    path("<str:pk>/share/", share_report, name="share_report"),
    path("public/<str:pk>/", public_reports, name="public_reports"),
    path("<str:pk>/delete/", delete_report, name="delete_report"),
]
