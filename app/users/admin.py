from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class UserAdminConfig(UserAdmin):
    search_fields = ('username', 'address', 'contract')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('-start_date',)
    list_display = ('username', 'role', 'address', 'contract', 'identifier', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Details', {'fields': ('role', 'address', 'contract', 'identifier')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'address', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
