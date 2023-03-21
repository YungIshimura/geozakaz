from django.urls import path

from zakaz.views import application_view

app_name = 'zakaz'

urlpatterns = [
    path('application/', application_view, name='application')
]

