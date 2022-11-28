from django import forms

def validate_file_extension(document):
    if not document.name.endswith('.pdf'):
        raise forms.ValidationError(u'File is not in PDF format')

class DocumentForm(forms.Form):
    type = forms.ChoiceField(
        label="Select a document type",
        choices=[("Bylaws", "Bylaws"),
        ("Strata Minute", "Strata Minute"),
        ("Financial", "Financial")],
        required=True,
        widget=forms.Select(),
        error_messages={'required': 'Please select a document type.'}
    )
    docfile = forms.FileField(label="Select the file to upload", validators=[validate_file_extension])

class ReportFilterForm(forms.Form):

    OPTIONS = [
        ("0", "Pet Restrictions"),
        ("1", "Rental Restrictions"),
        ("2", "Use of BBQ"),
        ("3", "Smoking Restrictions"),
        ]

    name = forms.CharField(label='Report Name', max_length=100)

    options = forms.MultipleChoiceField(
        choices=OPTIONS,
        widget=forms.CheckboxSelectMultiple(),
        label="Restrictions",
        required=True,
        error_messages={'required': 'Error: Please select at least one restriction.'}
    )