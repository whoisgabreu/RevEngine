from django.urls import path
from . import views

urlpatterns = [
    path('admin/tenants', views.tenant_list, name='tenant_list'),
    path('admin/tenants/criar', views.tenant_create, name='tenant_create'),
    path('admin/tenants/<int:pk>/editar', views.tenant_edit, name='tenant_edit'),
    path('admin/tenants/<int:pk>/excluir', views.tenant_delete, name='tenant_delete'),
    path('gerar-qr', views.gerar_qr, name='gerar_qr'),
    path('scan/<int:tenant_id>/', views.scan, name='scan'),
]
