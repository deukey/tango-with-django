from django.shortcuts import render, get_object_or_404
from .models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'top_categories': category_list, 'top_pages': page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html', {})


def category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    return render(request, 'rango/category.html', {'category': category})