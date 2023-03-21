from django.urls import path
from zakaz.views import application_view, application_pages_view

app_name = 'zakaz'

urlpatterns = [
    path('application/', application_view, name='application'),
    path('application_pages/', application_pages_view, name='application_pages')
]
