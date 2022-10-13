from django import forms

def validate_file_extension(document):
    if not document.name.endswith('.pdf'):
        raise forms.ValidationError(u'File is not in PDF format')

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file', validators=[validate_file_extension])

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
        error_messages={'required': 'Error: Please select at least one restriction.'
        }
    )