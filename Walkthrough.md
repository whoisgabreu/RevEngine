# ✅ RevEngine MVP — Walkthrough Completo

## O que foi construído

Sistema MVP completo de captação de leads via QR Code com arquitetura multi-tenant, usando **Django 6.0.4 + SQLite + Bootstrap 5**.

---

## Estrutura de arquivos criada

```
RevEngine/
├── venv/                         # Ambiente virtual Python
├── revengine/
│   ├── settings.py               # Config geral, AUTH_USER_MODEL, TEMPLATES
│   └── urls.py                   # Roteamento raiz
├── accounts/
│   ├── models.py                 # User (AbstractUser + tenant FK + is_admin)
│   ├── views.py                  # Login / logout com redirect por papel
│   ├── urls.py                   # /login, /logout
│   └── admin.py                  # User registrado no Django admin
├── tenants/
│   ├── models.py                 # Tenant, Lead, Visit
│   ├── views.py                  # CRUD tenants, gerar QR, scan
│   ├── urls.py                   # /admin/tenants, /gerar-qr, /scan/<id>/
│   └── admin.py                  # Modelos registrados no Django admin
├── core/
│   ├── views.py                  # admin_dashboard, cliente_dashboard
│   └── urls.py                   # /admin-dashboard, /cliente-dashboard
├── templates/
│   ├── base.html                 # Layout dark theme, Bootstrap 5, Inter font
│   ├── accounts/login.html
│   ├── core/
│   │   ├── admin_dashboard.html  # Métricas + tabela de tenants
│   │   └── cliente_dashboard.html
│   └── tenants/
│       ├── tenant_list.html
│       ├── tenant_form.html      # Criar / Editar (cria user junto)
│       ├── tenant_confirm_delete.html
│       ├── gerar_qr.html         # QR Code em base64 inline
│       ├── scan.html             # Form novo lead / botão retornante
│       └── scan_success.html
├── project_memory.md             # Documento de memória contínua do projeto
└── db.sqlite3                    # Banco SQLite gerado
```

---

## Como iniciar

```bash
cd /home/anthares/Documentos/Projetos/V4/RevEngine
venv/bin/python manage.py runserver 8000
```

Acesso: **http://127.0.0.1:8000/login**

---

## Credenciais

| Usuário | Senha    | Papel |
|---------|----------|-------|
| admin   | admin123 | Admin (acesso total) |

---

## Rotas disponíveis

| Rota | Descrição | Autenticação |
|------|-----------|--------------|
| `/login` | Login único | Pública |
| `/logout` | Encerrar sessão | Pública |
| `/admin-dashboard` | Dashboard com métricas | Admin |
| `/admin/tenants` | Lista de tenants | Admin |
| `/admin/tenants/criar` | Criar tenant + usuário | Admin |
| `/admin/tenants/<id>/editar` | Editar tenant | Admin |
| `/admin/tenants/<id>/excluir` | Excluir tenant | Admin |
| `/cliente-dashboard` | Painel do cliente | Cliente |
| `/gerar-qr` | Gerar QR Code (`?valor=XX.XX` opcional) | Cliente |
| `/scan/<tenant_id>/` | Captura de lead | Pública |
| `/django-admin/` | Admin nativo Django | Superuser |

---

## Fluxo validado no browser

1. ✅ **Login** — página carrega corretamente com design dark
2. ✅ **Admin Dashboard** — exibe métricas globais (total tenants, visitas, valor)
3. ✅ **Criar Tenant** — criou "Loja Beta" + usuário `beta_user` em único formulário
4. ✅ **Métricas atualizadas** — dashboard refletiu o novo tenant imediatamente
5. ✅ **Login como Cliente** — `beta_user` foi redirectionado para `/cliente-dashboard`
6. ✅ **QR Code fixo** — gerado em base64 na tela sem salvar no banco
7. ✅ **QR Code com valor** — `/gerar-qr?valor=75.50` — QR exibido com valor destacado
8. ✅ **Página de Scan** — formulário de lead renderizado para `/scan/1/` (público)

> **Gravação da demonstração:**
> ![Demonstração RevEngine](/home/anthares/.gemini/antigravity/brain/7c436d19-6c8c-4d78-b3f5-8169c53f6ce8/revengine_mvp_demo_1776951035212.webp)

---

## Decisões técnicas relevantes

- **QR Code gerado em memória** — biblioteca `qrcode` → `BytesIO` → base64 → renderizado diretamente no HTML. Nunca salvo no banco.
- **Lead identificado por `phone` + `tenant`** — `get_or_create` garante unicidade por tenant.
- **`is_admin` vs `is_staff`** — `is_admin` controla o fluxo da aplicação; `is_staff` é exclusivo para o `/django-admin/`.
- **Métricas via `annotate`** — `Count` e `Sum` no ORM, sem queries N+1.
- **Tenant + User criados juntos** — view `tenant_create` trata tudo em uma transação atômica implícita.
