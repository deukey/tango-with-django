# -*- coding: utf-8 -*-

from django import forms
from .models import Category, Page
from django.core.exceptions import ValidationError


def validate_can_make_slug(value):
    try:
        value.decode('ascii')
    # 한글을 걸러내기 위해서는 요게 필요
    except UnicodeDecodeError:
        raise ValidationError('영문이나 숫자가 하나라도 포함되어야 합니다.')
    else:
        if not any(c.isalnum() for c in value):
            raise ValidationError('영문이나 숫자가 하나라도 포함되어야 합니다.')
    # 이 방식만으로는 한글은 걸러내지 못함(아마도 파일 맨 위의 인코딩 선언 때문인듯)
    # 그래서 try except가 필요


# def validate_unique_slug(value):
#     try:
#         Category.objects.get(slug=value)
#         raise ValidationError('동일한 이름의 슬러그가 존재합니다. 카테고리 명을 바꿔주세요.')
#     except Category.DoesNotExist:
#         pass
    # TODO: 슬러그 숫자가 있으므로 이것은 지워도 될 듯


class CategoryForm(forms.ModelForm):
    korean_error_messages = {
        'required': '카테고리 이름을 꼭 넣어주세요.',
        'unique': '동일한 이름의 카테고리가 이미 존재합니다.',
        'max_length': '카테고리 이름이 너무 길어요.'
        }

    name = forms.CharField(help_text="카테고리 이름을 넣으세요(영문, 숫자만 가능).",
                           validators=[validate_can_make_slug],
                           error_messages=korean_error_messages)
    # slug = forms.SlugField(widget=forms.HiddenInput(), required=False,
    #                        validators=[validate_unique_slug])
    # validators= 인자를 넣으려는 경우에는 이런 식으로 필드를 따로 정의하는 수 밖에 없음
    # 즉 class Meta로는 다른 인자들은 모두 정의 가능하지만 validators 인자는 불가능

    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # def is_valid(self):
    #     valid = super(CategoryForm, self).is_valid()
    #
    #     if not valid:
    #         return valid
    #
    #     elif any(c.isalnum() for c in self.cleaned_data['name']):
    #         # 영문이나 숫자가 하나라도 포함되어 있어야 슬러그가 제대로 생성될 수 있으므로 이를 체크
    #         return True
    #
    #     else:
    #         self._errors['name'] = '영문이나 숫자가 하나라도 포함되어야 합니다.'
    #         return False

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    # title = forms.CharField(max_length=128, help_text="페이지의 제목을 넣으세요.")
    # url = forms.URLField(max_length=200, help_text="페이지의 URL을 넣으세요.")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = super(PageForm, self).clean()
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page
        fields = ('title', 'url',)
        korean_error_messages = {'required': '빈 항목을 꼭 채워주세요.'}
        help_texts = {
            'title': "페이지의 제목을 넣으세요.",
            'url': "페이지의 URL을 넣으세요."
        }
        error_messages = {
            'title': korean_error_messages,
            'url': korean_error_messages
        }

