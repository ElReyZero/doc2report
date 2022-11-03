import uuid
from django.db import models
from accounts.models import User

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    doc_page_length = models.IntegerField(default=0)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.docfile.name.split('/')[-1]
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.name