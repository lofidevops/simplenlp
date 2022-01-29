from django.apps import AppConfig
from nltk.corpus import stopwords

import wordy


class WordyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wordy"

    def ready(self):

        try:
            wordy.ENGLISH_STOP_WORDS = set(stopwords.words("english"))
        except LookupError:  # pragma: no cover
            wordy.ENGLISH_STOP_WORDS = set()
            wordy.logger.error(
                f"LookupError while loading stop words. Did you run initwordy before starting the site?"
            )
