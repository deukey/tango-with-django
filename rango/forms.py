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

        elif any(c.isalnum() for c in self.cleaned_data['name']):
            # 영문이나 숫자가 하나라도 포함되어 있어야 슬러그가 제대로 생성될 수 있으므로 이를 체크
            return True

        else:
            self._errors['name'] = '영문이나 숫자가 하나라도 포함되어야 합니다.'
            return False

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="페이지의 제목을 넣으세요.")
    url = forms.URLField(max_length=200, help_text="페이지의 URL을 넣으세요.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)