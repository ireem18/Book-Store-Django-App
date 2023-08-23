from django import forms
from .models import Publisher

class DateInput(forms.DateInput):
    input_type = 'date'

class PublisherForm(forms.ModelForm):

    class Meta:
        model = Publisher
        fields = ['name', 'code', 'started_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'max_length': 40}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code', 'max_length': 10}),
            'started_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Started Date'})
        }
