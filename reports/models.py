from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    name = models.CharField(max_length=255, blank=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.name = self.docfile.name.split('/')[-1]
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
