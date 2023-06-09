from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from geozakaz import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('zakaz.urls', namespace='zakaz')),
    path('', include('users.urls', namespace='users')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

