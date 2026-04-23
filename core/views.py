from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from django.contrib import messages
from tenants.models import Tenant, Lead, Visit
from accounts.models import User


@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('/cliente-dashboard')

    tenants = Tenant.objects.annotate(
        total_leads=Count('lead', distinct=True),
        total_visits=Count('visit', distinct=True),
        total_value=Sum('visit__value'),
    )

    total_tenants = tenants.count()
    total_visits = Visit.objects.count()
    total_value = Visit.objects.aggregate(total=Sum('value'))['total'] or 0

    return render(request, 'core/admin_dashboard.html', {
        'tenants': tenants,
        'total_tenants': total_tenants,
        'total_visits': total_visits,
        'total_value': total_value,
    })


@login_required
def cliente_dashboard(request):
    if request.user.is_admin:
        return redirect('/admin-dashboard')

    tenant = request.user.tenant
    if not tenant:
        messages.error(request, 'Seu usuário não está vinculado a nenhum cliente.')
        return redirect('/login')

    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    base_url = f"{scheme}://{host}/scan/{tenant.id}/"

    return render(request, 'core/cliente_dashboard.html', {
        'tenant': tenant,
        'base_url': base_url,
    })
