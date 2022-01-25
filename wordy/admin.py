from django.contrib import admin

from .models import Document
from .models import WordResult

admin.site.register(Document)
admin.site.register(WordResult)
