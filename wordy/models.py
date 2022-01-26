import os

from django.db import models
from django.conf import settings


class Document(models.Model):
    name = models.SlugField(unique=True)
    full_text = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        document_path = os.path.join(settings.MEDIA_ROOT, self.name + ".txt")
        self.full_text = open(document_path).read()
        super().save(*args, **kwargs)


class WordResult(models.Model):
    name = models.SlugField()
    count = models.IntegerField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    sample = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="wordresult_name_document", fields=["name", "document"]
            )
        ]

    def __str__(self):
        return f"{self.name}.{self.document}: {self.count}"
