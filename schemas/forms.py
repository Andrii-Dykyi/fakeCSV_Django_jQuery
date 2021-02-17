from django import forms
from .models import Schema, Column, DataSet


class SchemaCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control w-25'})
        self.fields['name'].label = 'Name'

    class Meta:
        model = Schema
        fields = ('name',)


class ColumnCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Column
        fields = ('name', 'type', 'start', 'end')


class DataSetCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_row'].widget.attrs.update({'class': 'form-control'})
        self.fields['num_row'].label = 'Rows:'

    class Meta:
        model = DataSet
        fields = ('num_row',)
