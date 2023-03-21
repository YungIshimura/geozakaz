from django.shortcuts import render


def application_view(request):
    return render(request, 'application.html')
