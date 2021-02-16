from django import forms
from .models import Schema, SchemaColumn


class SchemaCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control w-25'})
        self.fields['num_row'].widget.attrs.update({'class': 'form-control w-25'})
        self.fields['name'].label = 'Name'
        self.fields['num_row'].label = 'Row number'

    class Meta:
        model = Schema
        fields = ('name', 'num_row')


class SchemaColumnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = SchemaColumn
        fields = ('name', 'type', 'start', 'end')