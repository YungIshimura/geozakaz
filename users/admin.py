from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.utils.translation import gettext_lazy as _


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'company_slug', 'company_number_slug', 'first_name', 'last_name', 'patronymic', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'phone', 'company_slug', 'company_number_slug', 'company_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)
