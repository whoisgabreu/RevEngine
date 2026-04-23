from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_dashboard, name='home'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('cliente-dashboard', views.cliente_dashboard, name='cliente_dashboard'),
]
