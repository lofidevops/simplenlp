from django import forms


class UploadForm(forms.Form):
    document_file = forms.FileField(label="")
