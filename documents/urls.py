from django.urls import path
from .views import upload_document, delete_document

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path("<str:doc_pk>/", delete_document, name="delete_document"),
]
