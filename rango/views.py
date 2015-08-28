from django.shortcuts import render


def index(request):
    return render(request, 'rango/index.html', {'boldmessage': 'I am bold font.'})


def about(request):
    return render(request, 'rango/about.html', {})