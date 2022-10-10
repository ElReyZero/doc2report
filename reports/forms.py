from django import forms

def validate_file_extension(document):
    if not document.name.endswith('.pdf'):
        raise forms.ValidationError(u'File is not in PDF format')

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file', validators=[validate_file_extension])

