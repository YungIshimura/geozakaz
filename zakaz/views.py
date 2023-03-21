from django.shortcuts import render


def application_view(request):
    return render(request, 'application.html')


def application_pages_view(request):
    return render(request, 'application_pages.html')
