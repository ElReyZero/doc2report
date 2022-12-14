from django import forms


class DocumentForm(forms.Form):
    category = forms.ChoiceField(
        label="Select a document category",
        choices=[("Bylaws", "Strata Bylaws"),
        ("Minute", "Strata Minute"),
        ("Financial", "Financial Reports"),
        ("Depreciation", "Depreciation Reports")],
        required=True,
        widget=forms.Select(),
        error_messages={'required': 'Please select a document category.'}
    )


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