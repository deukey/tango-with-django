# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, related_name='pages')
    # If you need to create a relationship on a model that has not yet been defined,
    # you can use the name of the model, rather than the model object itself:
    # 즉 'Category'라고 넣어도 됨. 이게 유용할 때는 정의되지 않은 모델을 넣을 때와, 다른 앱의 모델을 넣을 때
    # 다른 앱의 모델을 넣을 때는 'otherapp.Category' 이런 식으로...
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
