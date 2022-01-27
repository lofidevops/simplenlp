from django.core.management import BaseCommand
import nltk


class Command(BaseCommand):
    help = "Initialise the environment for Wordy"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("Downloading NLTK data. This may take a while...")
        )
        nltk.download("popular")
        self.stdout.write(self.style.SUCCESS("Successfully downloaded NLTK data."))
