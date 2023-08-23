from django import forms

from .models import Writer, categories

from publisher.models import Publisher


class WriterForm(forms.ModelForm):

    class Meta:
        model = Writer
        fields = ['publisher', 'name', 'surname', 'age', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'max_length': 40}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname', 'max_length': 40}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'type': 'number'}),
            'categories': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choise One...'}, choices=categories)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'] = forms.ModelChoiceField(queryset=Publisher.objects.active(),
                                                          required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        clean_data = super().clean()
        age = clean_data.get('age')
        if age < 18:
            raise forms.ValidationError('This writer age should be greatter 18!')