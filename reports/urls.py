from django.urls import path
from .views import user_reports, delete_report

urlpatterns = [
    path('', user_reports, name='user_reports'),
    path("<str:pk>/", delete_report, name="delete_report"),
]
