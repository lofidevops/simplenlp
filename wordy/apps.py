from django.apps import AppConfig
from nltk.corpus import stopwords

import wordy


class WordyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wordy"

    def ready(self):
        try:
            wordy.ENGLISH_STOP_WORDS = set(stopwords.words("english"))
        except LookupError:
            wordy.ENGLISH_STOP_WORDS = set()
            wordy.logger.error(
                f"Stop words could not be loaded. Did you run initwordy?"
            )
