from django.urls import path

from .views import register_user, logout_account, view_agreement, login_company, login_user

app_name = 'users'

urlpatterns = [
    path('register/', register_user, name='user_register'),
    path('login_user', login_user, name='user_login'),
    path('login_company', login_company, name='company_login'),
    path('logout/', logout_account, name='user_logout'),
    path('agreement/', view_agreement, name='agreement')
]
