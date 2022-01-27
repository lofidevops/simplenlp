from django.shortcuts import render

from .forms import UploadForm
from .models import WordResult


def index(request):
    form = UploadForm()
    words_by_frequency = WordResult.get_words_by_frequency()
    context = {"form": form, "word_by_frequency": words_by_frequency}

    return render(request, "wordy/index.html", context)
