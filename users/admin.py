from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.utils.translation import gettext_lazy as _


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'company_slug', 'company_number_slug', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'phone_number', 'company_slug', 'company_number_slug', 'company_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ['email']


admin.site.register(User, CustomUserAdmin)
