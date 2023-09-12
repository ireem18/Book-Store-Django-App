from django import forms

from .models import Writer, categories

from publisher.models import Publisher


class WriterForm(forms.ModelForm):

    class Meta:
        model = Writer
        fields = ['publisher', 'name', 'surname', 'age', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'max_length': 40, 'required': True}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname', 'max_length': 40,
                                              'required': True}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'type': 'number'}),
            'categories': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choise One...',
                                              'required': True}, choices=categories)
        }
        help_texts = {
            'name': 'Please enter name',
            'surname': 'Please enter surname',
            'categories': 'Please choice categories',
            'age': 'Please enter age',
        }
        error_messages = {
            "name": {"max_length": "This writer's name is too long."},
            "surname": {"max_length": "This writer's surname is too long."}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'] = forms.ModelChoiceField(queryset=Publisher.objects.active(),
                                                          required=True, widget=forms.Select(attrs={'class': 'form-control'}),
                                                          help_text='Please choice publisher',
                                                          error_messages={"required": "This field is required!"})
