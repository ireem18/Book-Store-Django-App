from django import forms

from .models import Book
from writer.models import Writer
from publisher.models import Publisher

from ckeditor.widgets import CKEditorWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['publisher', 'writer', 'name', 'subject', 'description', 'count', 'page_count', 'publisher_date', 'isbn']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'max_length': 120, 'required': True}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'max_length': 120, 'required': True}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN', 'required': True}),
            'count': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Count'}),
            'page_count': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Page Count'}),
            'description': CKEditorWidget(),
            'publisher_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Publisher Date', 'required': True})
        }
        help_texts = {
            'name': 'Please enter name',
            'subject': 'Please enter subject',
            'description': 'Please enter description',
            'publisher_date': 'Please enter publisher date',
            'isbn': 'Please enter isbn',
            'count': 'Please enter count',
            'page_count': 'Please enter page count',
        }
        error_messages = {
            "name": {"max_length": "This writer's name is too long."},
            "subject": {"max_length": "This writer's subject is too long."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'] = forms.ModelChoiceField(queryset=Publisher.objects.active(),
                                                            required=True,
                                                            help_text='Please choice publisher',
                                                            widget=forms.Select(
                                                            attrs={'id': 'publisher_id',
                                                                  'class': 'form-control',
                                                                  'onchange': 'get_writers();'}))

        self.fields['writer'] = forms.ModelChoiceField(queryset=Writer.objects.none(),
                                                       required=True,
                                                       help_text='Please choice writer',
                                                       widget=forms.Select(
                                                       attrs={'id': 'writer_id',
                                                              'class': 'form-control'}))

        if 'publisher' in self.data and self.data.get('publisher') != '':
            publisher_id = self.data.get('publisher')
            self.fields['writer'].queryset = Writer.objects.active().filter(publisher_id=publisher_id).order_by('name')
        elif self.instance.pk:
            publisher_id = self.instance.publisher.id if self.instance.publisher else None
            self.fields['writer'].queryset = Writer.objects.active().filter(publisher_id=publisher_id).order_by('name')


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)