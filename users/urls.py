from django.urls import path
from .views import user_login, user_register, user_logout, view_agreement

app_name = 'users'

urlpatterns = [
    path('', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),
    path('agreement/', view_agreement, name='agreement'),
]