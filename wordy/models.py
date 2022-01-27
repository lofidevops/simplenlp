import os
from collections import namedtuple

from django.conf import settings
from django.db import models
from django.db.models import Sum
from nltk import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize

import wordy

ViewData = namedtuple("ViewData", ["word", "count", "occurrence"])


class Document(models.Model):
    name = models.SlugField(unique=True)
    full_text = models.TextField(
        blank=True
    )  # allows admin save as a workaround to uploading text files

    def __str__(self):
        return self.name

    @staticmethod
    def is_word_in_sentence(word, sentence):
        sentence_words = word_tokenize(sentence)
        return word in sentence_words

    @staticmethod
    def first_sentence_with_word(word, sentences):

        # find first sentence in list that contains word
        # otherwise return None
        return next(
            (s for s in sentences if Document.is_word_in_sentence(word, s)), None
        )

    def save(self, *args, **kwargs):
        document_path = os.path.join(settings.MEDIA_ROOT, self.name + ".txt")
        self.full_text = open(document_path).read()
        super().save(*args, **kwargs)

    def ingest(self):

        # delete existing results
        WordResult.objects.filter(document=self).delete()

        # parse the full text
        full_sentences = sent_tokenize(self.full_text)
        full_words = word_tokenize(self.full_text)
        frequencies = FreqDist(full_words)

        # save each word count, along with a sample sentence
        for word, count in frequencies.items():
            if word.isalpha() and word.casefold() not in wordy.ENGLISH_STOP_WORDS:
                sentence = Document.first_sentence_with_word(word, full_sentences)
                wr = WordResult(name=word, document=self, count=count, sample=sentence)
                wr.save()


class WordResult(models.Model):
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
        words_by_frequency = []

        # total count by word across all documents
        # (descending order, exclude words with a count of 1)
        # TODO: add a column for stem and group by that
        total_queryset = (
            WordResult.objects.values("name")
            .distinct()
            .annotate(total_count=Sum("count"))
            .filter(total_count__gt=1)
            .order_by("-total_count", "name")
        )

        # accumulate occurrences in distinct documents
        for result in total_queryset:
            name = result["name"]
            vd = ViewData(word=name, count=result["total_count"], occurrence={})

            for item in WordResult.objects.filter(name__exact=name):
                vd.occurrence[item.document.name] = item.sample

            words_by_frequency.append(vd)

        return words_by_frequency
