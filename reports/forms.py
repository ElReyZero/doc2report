from django import forms
import re

class NewReportForm(forms.Form):
    name = forms.CharField(label='Report Name', max_length=100)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Report name must be at least 3 characters long")
        return name

class GenerateReportFilterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('categories', None)
        super(GenerateReportFilterForm, self).__init__(*args, **kwargs)

    bylaw_options = [
        ("pets", "Pet Restrictions"),
        ("rental", "Rental Restrictions"),
        ("BBQ", "Use of BBQ"),
        ("smoking", "Smoking Restrictions"),
        ("other", "Other Restrictions")
    ]

    minutes_options = [
        ("Move in/out Fees", "Move In/Out Fees"),
        ("Strata Fee Increase", "Strata Fee Increase"),
        ("elevator", "Elevator"),
        ("building exterior", "Building Exterior"),
        ("leaks", "Leaks"),
        ("mould", "Mould"),
        ("legal/civil resolutions", "Legal/Civil Resolutions"),
        ("insurance", "Insurance"),
        ("plumbing", "Plumbing"),
        ("roof", "Roof"),
        ("security", "Security"),
        ("levy", "Levy"),
        ("windows", "Windows"),
        ("noise complaints", "Noise Complaints"),
        ("smoking complaints", "Smoking Complaints"),
        ("engineer reports", "Engineer Reports"),
        ("insurance claims", "Insurance Claims"),
        ("renovation requests", "Renovation Requests"),
        ("pests", "Pests"),
        ("fire inspections", "Fire Inspections")
    ]

    financial_options = [
        ("financial", "Yes")
    ]

    depreciation_options = [
        ("depreciation", "Yes")
    ]

    bylaws = forms.MultipleChoiceField(
        choices=bylaw_options,
        widget=forms.CheckboxSelectMultiple(),
        label="Bylaw Restrictions",
        required=False
    )

    minute = forms.MultipleChoiceField(
        choices=minutes_options,
        widget=forms.CheckboxSelectMultiple(),
        label="Strata Minute Restrictions",
        required=False
    )

    financial = forms.MultipleChoiceField(
        choices=financial_options,
        widget=forms.CheckboxSelectMultiple(),
        label="Financial Filter",
        required=False
    )

    depreciation = forms.MultipleChoiceField(
        choices=depreciation_options,
        widget=forms.CheckboxSelectMultiple(),
        label="Depreciation Filter",
        required=False
    )

    custom_question = forms.CharField(widget=forms.Textarea(), label="Custom Question", required=False)

    price_calculation = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        bylaws = cleaned_data.get("bylaws")
        minutes = cleaned_data.get("minutes")
        financial = cleaned_data.get("financial")
        depreciation = cleaned_data.get("depreciation")
        custom_question = cleaned_data.get("custom_question")
        if not bylaws and not minutes and not financial and not depreciation and custom_question == "":
            raise forms.ValidationError("You must select at least one filter or ask a custom question")
        if custom_question != "":
            custom_question = custom_question.replace("\r", "").split("\n")
            custom_question_cleaned = []
            for question in custom_question:
                question = re.split("\d\.", question)
                if len(question) != 2:
                    raise forms.ValidationError("Invalid custom question format")
                question = question[1].strip()
                try:
                    if question[-1] != "?" and question[-1] != ")":
                        question += "?"
                except IndexError:
                    raise forms.ValidationError("Invalid custom question format")
                custom_question_cleaned.append(question)
            cleaned_data["custom_question"] = custom_question_cleaned
        return cleaned_data