from django.urls import path


from zakaz.views import view_order_pages, view_change_order_status, view_order_cadastral, view_order, view_download, download_igdi_docx, \
     download_igi_docx

app_name = 'zakaz'

urlpatterns = [
    path('order/<slug:company_slug>/<slug:company_number_slug>/', view_order_cadastral, name='cadastral'),
    path('order/<slug:company_slug>/<slug:company_number_slug>/form',view_order, name='order'),
    path('order_pages/', view_order_pages, name='order_pages'),
    path('change_order_status/<slug:slug>/', view_change_order_status, name="change_order_status"),
    path('download/', view_download),
    path('download__igdi_docx/', download_igdi_docx, name='download_igdi_docx'),
    path('download_igi_docx/', download_igi_docx, name='download_igi_docx'),
]
