from django.urls import path
from .views import upload_document, delete_document

urlpatterns = [
    path('', upload_document, name='upload_document'),
    path('success/', upload_document, name='success'),
    path("<str:pk>/", view=delete_document, name="delete_document"),
]
