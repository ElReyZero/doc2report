from django.urls import path
from .views import *

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path('<str:doc_pk>/', view_document, name='view_document'),
    path("<str:doc_pk>/delete/", delete_document, name="delete_document"),
]
