from django.urls import path
from .views import generate_report, upload_document, delete_document

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path("<str:pk>/", delete_document, name="delete_document"),
    path('<str:pk>/generate/', generate_report, name='generate_report'),
]
