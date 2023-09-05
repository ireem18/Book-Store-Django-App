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
        self.fields['publisher'] = forms.ModelChoiceField(queryset=Publisher.objects.active(),
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
            self.fields['writer'].queryset = Writer.objects.active().filter(publisher_id=publisher_id).order_by('name')
        elif self.instance.pk:
            publisher_id = self.instance.publisher.id if self.instance.publisher else None
            self.fields['writer'].queryset = Writer.objects.active().filter(publisher_id=publisher_id).order_by('name')

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        clean_data = super().clean()
        instance.publisher = clean_data.get('publisher')
        instance.writer = clean_data.get('writer')
        instance.name = clean_data.get('name')
        instance.subject = clean_data.get('subject')
        instance.description = clean_data.get('description')
        instance.isbn = clean_data.get('isbn')
        instance.page_count = clean_data.get('page_count')
        instance.count = clean_data.get('count')
        instance.publisher_date = clean_data.get('publisher_date')
        if commit:
            instance.save()
        return instance

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)