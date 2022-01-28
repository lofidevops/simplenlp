from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render
from django.utils.text import slugify

from .forms import UploadForm
from .models import Document, WordResult


def handle_upload(f: UploadedFile):
    """Store uploaded file as a document. Existing documents (determined by filename) are overwritten.
    Non-text files are rejected."""

    if f.content_type != "text/plain":
        raise NotImplementedError(
            f"Filetype not handled. Please upload a text/plain file."
        )

    name = slugify(f.name.replace(".txt", ""))
    content = f.read().decode(
        "utf-8"
    )  # we assume small files, so we don't use f.chunk()

    existing_queryset = Document.objects.filter(name__exact=name)

    # create new document, or overwrite existing one
    if len(existing_queryset) == 0:
        document = Document(name=name, full_text=content)
    else:
        document = existing_queryset[0]
        document.full_text = content

    document.save()

    # process document
    try:
        document.ingest()
    except LookupError:
        raise LookupError(
            "LookupError while running ingest function. Did you run initwordy before starting the site?"
        )


def index(request):
    """On GET, generate app form and results. On POST, process the uploaded text file."""

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload(request.FILES["document_file"])

    form = UploadForm()  # reset form
    words_by_frequency = WordResult.get_words_by_frequency()
    context = {"form": form, "word_by_frequency": words_by_frequency}

    return render(request, "wordy/index.html", context)
