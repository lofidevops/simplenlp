from django.test import TestCase
from .models import Document, WordResult, ViewData


class EmptyDatabaseTestCase(TestCase):
    def setUp(self):
        pass  # no database entries

    def test_results_are_empty(self):
        result = WordResult.get_words_by_frequency()
        self.assertEqual(result, {})


class SingleDocumentWithoutIngestTestCase(TestCase):
    def setUp(self):
        doc = Document(name="test", full_text="Full text.")
        doc.save()

    def test_results_are_empty(self):
        result = WordResult.get_words_by_frequency()
        self.assertEqual(result, {})

    def test_document_string(self):
        doc = Document.objects.first()
        self.assertEqual(str(doc), "test")


class ConstructedWordResultTestCase(TestCase):
    def setUp(self):
        doc = Document(name="test", full_text="Full text.")
        doc.save()
        wr = WordResult(name="world", count=2, sample="Hello world.", document=doc)
        wr.save()

    def test_wordresult_string(self):
        wr = WordResult.objects.first()
        self.assertEqual(str(wr), "world.test: 2")


class TwoUniqueWordsTestCase(TestCase):
    def setUp(self):
        doc = Document(name="test", full_text="Full text.")
        doc.save()
        doc.ingest()

    def test_results_are_empty(self):
        result = WordResult.get_words_by_frequency()
        self.assertEqual(result, {})


class TwoIdenticalWordsTestCase(TestCase):
    def setUp(self):
        doc = Document(name="test", full_text="Hello Hello.")
        doc.save()
        doc.ingest()

    def test_results_are_populated(self):
        result = WordResult.get_words_by_frequency()
        target = {
            "Hello": ViewData(
                word="Hello", count=2, occurrence={"test": "Hello Hello."}
            )
        }

        self.assertEqual(result, target)


class TwoDocumentsUniqueWordsTestCase(TestCase):
    def setUp(self):
        doc1 = Document(name="test1", full_text="One two.")
        doc1.save()
        doc1.ingest()
        doc2 = Document(name="test2", full_text="Three, four.")
        doc2.save()
        doc2.ingest()

    def test_results_are_empty(self):
        result = WordResult.get_words_by_frequency()
        self.assertEqual(result, {})


class TwoDocumentsWordsDuplicatedAcrossSentence(TestCase):
    def setUp(self):
        doc1 = Document(name="test1", full_text="One two.")
        doc1.save()
        doc1.ingest()
        doc2 = Document(name="test2", full_text="Hello, Hello.")
        doc2.save()
        doc2.ingest()

    def test_results_are_populated(self):
        result = WordResult.get_words_by_frequency()
        target = {
            "Hello": ViewData(
                word="Hello", count=2, occurrence={"test2": "Hello, Hello."}
            )
        }

        self.assertEqual(result, target)


class TwoDocumentsWordsDuplicatedAcrossDocuments(TestCase):
    def setUp(self):
        doc1 = Document(name="test1", full_text="One Hello.")
        doc1.save()
        doc1.ingest()
        doc2 = Document(name="test2", full_text="Hello, four.")
        doc2.save()
        doc2.ingest()

    def test_results_are_populated(self):
        result = WordResult.get_words_by_frequency()
        target = {
            "Hello": ViewData(
                word="Hello",
                count=2,
                occurrence={"test1": "One Hello.", "test2": "Hello, four."},
            )
        }

        self.assertEqual(result, target)
