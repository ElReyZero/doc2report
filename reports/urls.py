from django.urls import path
from .views import generate_report, upload_document, delete_document

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path('generate/', generate_report, name='generate_report'),
    path("<str:pk>/", view=delete_document, name="delete_document"),
]
