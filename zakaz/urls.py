from django.urls import path

from zakaz.views import (view_order_pages, view_change_order_status,
                         view_order_cadastral, view_order, view_rates,
                         download_igi_docx, city_autocomplete,
                         ajax_validate_cadastral_number, region_autocomplete,
                         area_autocomplete,
                         download_map, download_xlsx, download_igdi_docx,
                         download_all_docx, purpose_building_autocomplete,
                         get_square)

app_name = 'zakaz'

urlpatterns = [
    path('validate_cadastral', ajax_validate_cadastral_number,
         name='ajax_validate_cadastral_number'),
    path('region_autocomlete', region_autocomplete, name='region_autocomplete'),
    path('area_autocomlete', area_autocomplete, name='area_autocomplete'),
    path('city_autocomplete', city_autocomplete, name='city_autocomplete'),
    path('order/<slug:company_slug>/<slug:company_number_slug>/',
         view_order_cadastral, name='cadastral'),
    path('order/<slug:company_slug>/<slug:company_number_slug>/form/',
         view_order, name='order'),
    path('order_pages/<slug:company_number_slug>/',
         view_order_pages, name='order_pages'),
    path('change_order_status/<int:order_id>/',
         view_change_order_status, name="change_order_status"),
    path('rates', view_rates, name='rates'),
    path('download_igi_docx/<int:pk>/',
         download_igi_docx, name='download_igi_docx'),
    path('download_igdi_docx/<int:pk>/',
         download_igdi_docx, name='download_igdi_docx'),
    path('download_all_docx/<int:pk>/',
         download_all_docx, name='download_all_docx'),
    path('download_map/<int:pk>/', download_map, name='download_map'),
    path('download_xlsx/<int:pk>/', download_xlsx, name='download_xlsx'),
    path('purpose_building_autocomplete/', purpose_building_autocomplete,
         name='purpose_building_autocomplete'),
    path('get_square/', get_square, name='get_square')
]
