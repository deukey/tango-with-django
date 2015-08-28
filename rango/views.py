from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'rango/index.html', {'boldmessage': 'I am bold font.'})


def about(request):
    return HttpResponse('This is about page.<br/><a href="/rango">Index</a>')