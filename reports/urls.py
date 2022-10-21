from django.urls import path
from .views import user_reports, delete_report, generated_report

urlpatterns = [
    path('', user_reports, name='user_reports'),
    path("<str:pk>/", generated_report, name="generated_report"),
    path("<str:pk>/delete/", delete_report, name="delete_report"),
]
