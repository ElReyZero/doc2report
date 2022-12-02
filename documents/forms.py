from django import forms

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