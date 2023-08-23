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
            'description': CKEditorWidget(),
            'publisher_date': DateInput(attrs={'class': 'form-control', 'placeholder': 'Publisher Date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'] = forms.ModelChoiceField(queryset=Publisher.objects.filter(active=True),
                               required=True,
                               widget=forms.Select(
                               attrs={'id': 'publisher_id',
                                      'class': 'form-control',
                                      'onchange': 'get_writers();'}))

        self.fields['writer'] = forms.ModelChoiceField(queryset=Writer.objects.none(),
                               required=True,
                               widget=forms.Select(
                               attrs={'id': 'writer_id',
                                      'class': 'form-control'}))

        if 'publisher' in self.data:
            publisher_id = self.data.get('publisher')
            self.fields['writer'].queryset = Writer.objects.filter(publisher_id=publisher_id, active=True).order_by('name')
        elif self.instance.pk:
            self.fields['writer'].queryset = self.instance.publisher.writer_set.order_by('name')

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)