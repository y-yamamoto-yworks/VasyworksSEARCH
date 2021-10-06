"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class SearchBuildingIdForm(forms.Form):
    """
    建物ID検索フォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['building_id'] = forms.CharField(
            label=_('建物ID'),
            required=True,
            widget=forms.TextInput(attrs={
                'style': 'text-align: right;',
                'pattern': '^[0-9]+$'}),
        )
        self.fields['building_id'].widget.attrs['v-model'] = 'building_id'

        for key in self.fields.keys():
            field = self.fields[key]
            field.widget.attrs['ref'] = key
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
