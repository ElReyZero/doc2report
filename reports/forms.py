from django import forms


class NewReportForm(forms.Form):
    name = forms.CharField(label='Report Name', max_length=100)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Report name must be at least 3 characters long")
        return name