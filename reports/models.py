import uuid
from django.db import models
from accounts.models import User
# Create your models here.

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    can_generate = models.BooleanField(default=False)
    already_generated = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default="Created")

    def __str__(self):
        return self.name