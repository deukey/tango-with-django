# -*- coding: utf-8 -*-

from django import forms
from .models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="카테고리 이름을 넣으세요(영문, 숫자만 가능).")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    def is_valid(self):
        valid = super(CategoryForm, self).is_valid()

        if not valid:
            return valid

        else:
            try:
                self.cleaned_data['name'].decode('ascii')
            except UnicodeDecodeError:
                self._errors['non_ascii'] = '카테고리 이름은 영문이나 숫자, 하이픈만 가능합니다.'
                # raise forms.ValidationError('bad value')
                return False

        return True

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="페이지의 제목을 넣으세요.")
    url = forms.URLField(max_length=200, help_text="페이지의 URL을 넣으세요.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)