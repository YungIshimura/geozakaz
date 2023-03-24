from django.urls import path

from zakaz.views import view_order, view_order_pages, view_change_order_status

app_name = 'zakaz'

urlpatterns = [
    path('order/<int:company_id>/', view_order, name='order'),
    path('order_pages/', view_order_pages, name='order_pages'),
    path('change_order_status/<slug:slug>/', view_change_order_status, name="change_order_status")
]
