from collections import namedtuple

from django.db.models import Sum
from django.shortcuts import render

from .forms import UploadForm
from .models import WordResult

ViewData = namedtuple("ViewData", ["word", "count", "occurrence"])


def index(request):

    form = UploadForm()
    word_by_frequency = []

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

        word_by_frequency.append(vd)

    context = {"form": form, "word_by_frequency": word_by_frequency}

    return render(request, "wordy/index.html", context)
