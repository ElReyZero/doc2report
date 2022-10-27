import uuid
from django.db import models
from documents.models import Document
from accounts.models import User
# Create your models here.

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_filter = models.BooleanField()
    rental_filter = models.BooleanField()
    bbq_filter = models.BooleanField()
    smoking_filter = models.BooleanField()
    predictions = models.JSONField(null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name