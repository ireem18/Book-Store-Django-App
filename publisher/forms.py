from django import forms
from .models import Publisher

class DateInput(forms.DateInput):
    input_type = 'date'

class PublisherForm(forms.ModelForm):

    class Meta:
        model = Publisher
        fields = ['name', 'code', 'started_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'max_length': 40, 'required':True}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code', 'max_length': 10, 'required':True}),
            'started_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Started Date'})
        }
        help_texts = {
            'name': 'Please enter name',
            'code': 'Please enter code',
            'started_date': 'Please enter started_date'
        }
        error_messages = {
            "name": {"max_length": "This writer's name is too long.", "required": "This field is required!"},
            "code": {"max_length": "This writer's code is too long.", "required": "This field is required!"}
        }

    def save(self, commit=True):
        instance = super(PublisherForm, self).save(commit=False)
        clean_data = super().clean()
        instance.name = clean_data.get('name')
        instance.code = clean_data.get('code')
        instance.started_date = clean_data.get('started_date')
        if commit:
            instance.save()
        return instance