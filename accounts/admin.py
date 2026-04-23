from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('RevEngine', {'fields': ('tenant', 'is_admin')}),
    )
    list_display = ('username', 'email', 'tenant', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'tenant')
