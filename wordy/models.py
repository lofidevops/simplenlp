from collections import namedtuple

from django.db import models
from django.db.models import Sum
from nltk import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize

import wordy

ViewData = namedtuple(
    "ViewData", ["word", "count", "occurrence"]
)  # simple structure to store a summary of results


class Document(models.Model):
    """A document with full text, ready for ingestion."""

    name = models.SlugField(unique=True)
    full_text = models.TextField()

    def __str__(self):
        return self.name

    def ingest(self):
        """Perform natural language processing on this document and store the results. Previous results for this
        document are replaced."""

        # delete existing results
        WordResult.objects.filter(document=self).delete()

        # calculate word frequencies
        full_words = word_tokenize(self.full_text)
        frequencies = FreqDist(full_words)

        # accumulate samples for each word
        # we iterate by sentence to efficiently cover all samples
        results_by_word = {}
        for sentence in sent_tokenize(self.full_text):
            for word in word_tokenize(sentence):
                if (
                    word.isalpha()
                    and word.casefold() not in wordy.ENGLISH_STOP_WORDS
                    and word not in results_by_word
                ):
                    results_by_word[word] = WordResult(
                        name=word,
                        document=self,
                        count=frequencies[word],
                        sample=sentence,
                    )

        # store results with samples
        WordResult.objects.bulk_create(results_by_word.values())


class WordResult(models.Model):
    """Measurements for a single word in a single document."""

    name = models.SlugField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    count = models.IntegerField()
    sample = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="wordresult_name_document", fields=["name", "document"]
            )
        ]

    def __str__(self):
        return f"{self.name}.{self.document}: {self.count}"

    @classmethod
    def get_words_by_frequency(cls):
        """Generate results across all documents in dictionary format. Words are ordered by total count. Each entry
        includes a sample sentence from each document the word appears in."""

        # calculate total count by word across all documents
        # (descending order, exclude words with a count of 1)
        total_queryset = (
            WordResult.objects.values("name")
            .distinct()
            .annotate(total_count=Sum("count"))
            .filter(total_count__gt=1)
            .order_by("-total_count", "name")
        )

        # convert results to dictionary
        result = {}
        for item in total_queryset:
            name = item["name"]
            result[name] = ViewData(word=name, count=item["total_count"], occurrence={})

        # collect all distinct samples
        sample_queryset = WordResult.objects.values(
            "name", "document__name", "sample"
        ).order_by("name", "document__name")

        # add samples to results
        for item in sample_queryset:
            name = item["name"]
            document = item["document__name"]

            if name in result.keys():
                result[name].occurrence[document] = item["sample"]

        return result
