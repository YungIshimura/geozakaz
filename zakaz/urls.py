from django.urls import path

from django.contrib import admin
from zakaz.views import view_application, view_application_pages

app_name = 'zakaz'

urlpatterns = [
    path('application/', view_application, name='application'),
    path('application_pages/', view_application_pages, name='application_pages'),
]
