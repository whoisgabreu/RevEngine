from django.contrib import admin
from .models import Tenant, Lead, Visit


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cohort', 'created_at')
    search_fields = ('name', 'cohort')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'tenant', 'created_at')
    list_filter = ('tenant',)
    search_fields = ('name', 'phone')


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'tenant', 'value', 'created_at')
    list_filter = ('tenant',)
