# -*- coding: utf-8 -*-

from django import forms
from .models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="카테고리 이름을 넣으세요(영문, 숫자만 가능).")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="페이지의 제목을 넣으세요.")