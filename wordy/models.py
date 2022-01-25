from django.db import models


class Document(models.Model):
    name = models.SlugField(unique=True)
    full_text = models.TextField()

    def __str__(self):
        return self.name


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
