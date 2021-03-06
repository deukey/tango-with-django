# -*- coding: utf-8 -*-

from django import forms
from .models import Category, Page, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def validate_can_make_slug(value):
    try:
        value.decode('ascii')
    # 한글을 걸러내기 위해서는 요게 필요
    except UnicodeDecodeError:
        raise ValidationError('영문을 제외한 문자는 사용할 수 없어요.')
    else:
        if not any(c.isalnum() for c in value):
            raise ValidationError('영문이나 숫자가 하나라도 포함되어야 합니다.')
    # 이 방식만으로는 한글은 걸러내지 못함(아마도 파일 맨 위의 인코딩 선언 때문인듯)
    # 그래서 try except가 필요

    # TODO: 현재 버그 존재(한글+영문일 경우 제대로 동작 안함)


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
    # validators= 인자를 넣으려는 경우에는 이런 식으로 필드를 따로 정의하는 수 밖에 없음
    # 즉 class Meta로는 다른 인자들은 모두 정의 가능하지만 validators 인자는 불가능

    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)
    # 정의한 이유는 하단에서 설명(fields 정의에서)

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

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        slugged_name = slugify(cleaned_data.get('name'))

        if slugged_name != '':
            try:
                Category.objects.get(slug=slugged_name)
            except Category.DoesNotExist:
                cleaned_data['slug'] = slugged_name
            else:
                num = 0
                while True:
                    new_name = slugged_name
                    try:
                        num += 1
                        new_name += str(num)
                        Category.objects.get(slug=new_name)
                    except Category.DoesNotExist:
                        cleaned_data['slug'] = new_name
                        break

        return cleaned_data
    # http://stackoverflow.com/questions/18371457/modelform-override-clean-method 참조

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        # 여기에 include 되지 않은 모델들은 clean() 과정을 거치지 않고 저장됨
        # 따라서 clean()을 통하여 데이터 후처리를 하기 위해서는 여기에 해당 모델을 반드시 정의해야 함


class PageForm(forms.ModelForm):
    # title = forms.CharField(max_length=128, help_text="페이지의 제목을 넣으세요.")
    # url = forms.URLField(max_length=200, help_text="페이지의 URL을 넣으세요.")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # def clean(self):
    #     cleaned_data = super(PageForm, self).clean()
    #     url = cleaned_data.get('url')
    #
    #     if url and not url.startswith('http://'):
    #         url = 'http://' + url
    #         cleaned_data['url'] = url
    #
    #     return cleaned_data
    # 이거 안 넣어도 자동으로 처리됨

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


class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'url', 'category',)


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'password': forms.PasswordInput,
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)