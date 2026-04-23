import io
import base64
import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tenant, Lead, Visit
from accounts.models import User


# ─── Admin: CRUD Tenants ────────────────────────────────────────────────────

@login_required
def tenant_list(request):
    if not request.user.is_admin:
        return redirect('/cliente-dashboard')
    tenants = Tenant.objects.all()
    return render(request, 'tenants/tenant_list.html', {'tenants': tenants})


@login_required
def tenant_create(request):
    if not request.user.is_admin:
        return redirect('/cliente-dashboard')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        cohort = request.POST.get('cohort', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([name, cohort, username, password]):
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'tenants/tenant_form.html', {'action': 'Criar'})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return render(request, 'tenants/tenant_form.html', {'action': 'Criar'})

        tenant = Tenant.objects.create(name=name, cohort=cohort)
        user = User.objects.create_user(username=username, password=password, tenant=tenant, is_admin=False)
        messages.success(request, f'Tenant "{name}" criado com usuário "{username}".')
        return redirect('/admin/tenants')

    return render(request, 'tenants/tenant_form.html', {'action': 'Criar'})


@login_required
def tenant_edit(request, pk):
    if not request.user.is_admin:
        return redirect('/cliente-dashboard')
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        tenant.name = request.POST.get('name', tenant.name).strip()
        tenant.cohort = request.POST.get('cohort', tenant.cohort).strip()
        tenant.save()
        messages.success(request, 'Tenant atualizado.')
        return redirect('/admin/tenants')
    return render(request, 'tenants/tenant_form.html', {'action': 'Editar', 'tenant': tenant})


@login_required
def tenant_delete(request, pk):
    if not request.user.is_admin:
        return redirect('/cliente-dashboard')
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        tenant.delete()
        messages.success(request, 'Tenant excluído.')
        return redirect('/admin/tenants')
    return render(request, 'tenants/tenant_confirm_delete.html', {'tenant': tenant})


# ─── Cliente: Gerar QR Code ─────────────────────────────────────────────────

@login_required
def gerar_qr(request):
    if request.user.is_admin:
        return redirect('/admin-dashboard')

    tenant = request.user.tenant
    if not tenant:
        messages.error(request, 'Sem tenant vinculado.')
        return redirect('/login')

    valor = request.GET.get('valor', '').strip()
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'

    scan_url = f"{scheme}://{host}/scan/{tenant.id}/"
    if valor:
        scan_url += f"?valor={valor}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(scan_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'tenants/gerar_qr.html', {
        'qr_b64': qr_b64,
        'scan_url': scan_url,
        'valor': valor,
        'tenant': tenant,
    })


# ─── Scan: Captura de Lead ───────────────────────────────────────────────────

def scan(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    valor_str = request.GET.get('valor', '').strip()
    valor = None
    if valor_str:
        try:
            valor = float(valor_str)
        except ValueError:
            valor = None

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        name = request.POST.get('name', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()

        if not phone:
            messages.error(request, 'Telefone é obrigatório.')
            return render(request, 'tenants/scan.html', {
                'tenant': tenant, 'valor': valor, 'show_form': True
            })

        lead, created = Lead.objects.get_or_create(
            phone=phone,
            tenant=tenant,
            defaults={'name': name, 'birth_date': birth_date or '2000-01-01'},
        )

        Visit.objects.create(lead=lead, tenant=tenant, value=valor)

        return render(request, 'tenants/scan_success.html', {
            'lead': lead,
            'valor': valor,
            'tenant': tenant,
            'novo': created,
        })

    # GET: verificar se número já está cadastrado via query param
    phone_param = request.GET.get('phone', '').strip()
    if phone_param:
        lead_exists = Lead.objects.filter(phone=phone_param, tenant=tenant).exists()
        return render(request, 'tenants/scan.html', {
            'tenant': tenant,
            'valor': valor,
            'show_form': not lead_exists,
            'phone_prefill': phone_param,
        })

    return render(request, 'tenants/scan.html', {
        'tenant': tenant,
        'valor': valor,
        'show_form': True,
    })
