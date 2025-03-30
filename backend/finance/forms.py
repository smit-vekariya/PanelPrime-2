from django import forms
from finance.models import ITCompany


class ITCompanyForm(forms.ModelForm):
    apply_on = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    interview_on = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = ITCompany
        fields = "__all__"