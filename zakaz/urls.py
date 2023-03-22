from django.urls import path

from zakaz.views import view_order, view_order_pages, change_order_status_view

app_name = 'zakaz'

urlpatterns = [
    path('order/', view_order, name='order'),
    path('order_pages/', view_order_pages, name='order_pages'),
    path('cahge_order_status/<int:pk>/', change_order_status_view, name="change_order_status")
]
