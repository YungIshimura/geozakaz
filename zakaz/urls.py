from django.urls import path


from zakaz.views import (view_order_pages, view_change_order_status, view_order_cadastral,
                         view_order, view_download,
                         ajax_validate_cadastral_number,
                         # download_igi_docx, download_igdi_docx
                            )
from zakaz.views import view_order_pages, view_change_order_status, view_order_cadastral, view_order, download_igi_docx, \
    ajax_validate_cadastral_number

app_name = 'zakaz'

urlpatterns = [
    path('validate_username', ajax_validate_cadastral_number, name='ajax_validate_cadastral_number'),
    path('order/<slug:company_slug>/<slug:company_number_slug>/', view_order_cadastral, name='cadastral'),
    path('order/<slug:company_slug>/<slug:company_number_slug>/form', view_order, name='order'),
    path('order_pages/<slug:company_number_slug>/', view_order_pages, name='order_pages'),
    path('change_order_status/<int:order_id>/', view_change_order_status, name="change_order_status"),
    path('download_igi_docx/<int:pk>/', download_igi_docx, name='download_igi_docx'),
    path('download/', view_download),
    # path('download__igdi_docx/', download_igdi_docx, name='download_igdi_docx'),
    # path('download_igi_docx/', download_igi_docx, name='download_igi_docx'),
]
