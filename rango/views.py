# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Page
from .forms import CategoryForm, PageForm, PageEditForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'top_categories': category_list, 'top_pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True

    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    return render(request, 'rango/index.html', context_dict)


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    return render(request, 'rango/about.html', {'visits': count})


def category(request, category_name_slug):
    cat = get_object_or_404(Category, slug=category_name_slug)
    context_dict = {'category': cat, 'cat_slug': category_name_slug}
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('rango.views.index')
        else:
            print form.errors

    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def edit_category(request, category_name_slug):
    cat = get_object_or_404(Category, slug=category_name_slug)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            cat = form.save()
            return redirect('rango.views.category', category_name_slug=cat.slug)
    else:
        form = CategoryForm(instance=cat)
    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_category.html', context_dict)


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return redirect('rango.views.category', category_name_slug=category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


@login_required
def edit_page(request, category_name_slug, pk):
    page = get_object_or_404(Page, pk=pk)

    if request.method == 'POST':
        form = PageEditForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
            return redirect('rango.views.category', category_name_slug=category_name_slug)
    else:
        form = PageEditForm(instance=page)
    context_dict = {'form': form, 'category': page.category}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             registered = True
#         else:
#             print user_form.errors, profile_form.errors
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request, 'rango/register.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
#
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('rango.views.index')
#             else:
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             print "Invalid login details: {0}, {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("로그인하셨으므로 이 글을 보실 수 있습니다!!!")


# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('rango.views.index')