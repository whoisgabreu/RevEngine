# 📘 Project Memory — RevEngine

## 🧾 Visão Geral

Sistema MVP de captação de leads via QR Code com arquitetura multi-tenant.
Permite que empresas (tenants) gerem QR Codes, capturem leads no momento do scan e visualizem métricas no dashboard administrativo.

---

## ⚙️ Stack Atual

- **Design System:** Cyber Neon (Black background #000000, White text #FFFFFF, Neon Green #39FF14)
- **Framework:** Django 6.0.4
- **Banco:** SQLite (`db.sqlite3`)
- **ORM:** Django ORM
- **Frontend:** Django Templates + Bootstrap 5.3 (CDN)
- **QR Code:** biblioteca `qrcode` + `pillow` (geração dinâmica em base64)
- **Autenticação:** sistema padrão do Django com `AbstractUser` customizado
- **Ambiente Python:** `venv/` na raiz do projeto

---

## 📅 Histórico de Alterações

### [2026-04-23] — Novo Visual (Neon Green & Black)

**Descrição:**
Atualização completa da paleta de cores para um visual de alto contraste e estética premium.
- Fundo totalmente preto (#000000)
- Textos base em Branco Puro (#FFFFFF)
- Elementos de destaque e indicadores em Verde Neon (#39FF14)
- Adição de efeitos de brilho (glow) em elementos primários.

**Arquivos afetados:**
- `templates/base.html` — Atualização de variáveis CSS e estilos globais.
- `project_memory.md` — Atualização da documentação da stack visual.

**Motivo:**
Melhoria da legibilidade e modernização da interface conforme pedido do usuário.

**Impacto:**
Interface mais vibrante e legivel em ambientes de baixa luminosidade, mantendo a sensação premium.

---

### [2026-04-23] — Criação do MVP completo

**Descrição:**
Projeto Django criado do zero com 3 apps (`core`, `accounts`, `tenants`), modelos, views, URLs e templates completos.

**Arquivos afetados:**
- `revengine/settings.py` — configurações gerais, AUTH_USER_MODEL, TEMPLATES dir
- `revengine/urls.py` — roteamento raiz para os 3 apps
- `accounts/models.py` — User customizado (`AbstractUser` + `tenant` FK + `is_admin`)
- `accounts/views.py` — login/logout com redirecionamento por papel
- `accounts/urls.py` — `/login`, `/logout`
- `accounts/admin.py` — registro do User no admin Django
- `tenants/models.py` — Tenant, Lead, Visit
- `tenants/views.py` — CRUD tenants, geração de QR Code (base64 inline), scan/captura de lead
- `tenants/urls.py` — `/admin/tenants`, `/gerar-qr`, `/scan/<tenant_id>/`
- `tenants/admin.py` — registro dos modelos no admin Django
- `core/views.py` — admin_dashboard (métricas agregadas), cliente_dashboard
- `core/urls.py` — `/admin-dashboard`, `/cliente-dashboard`
- `templates/base.html` — layout dark theme, Bootstrap 5, Inter font, navbar dinâmica por papel
- `templates/accounts/login.html`
- `templates/core/admin_dashboard.html`
- `templates/core/cliente_dashboard.html`
- `templates/tenants/tenant_list.html`
- `templates/tenants/tenant_form.html` — create/edit (condicional: campos de usuário só no create)
- `templates/tenants/tenant_confirm_delete.html`
- `templates/tenants/gerar_qr.html` — exibe QR code em base64 inline
- `templates/tenants/scan.html` — formulário de cadastro p/ lead novo / botão de confirmação p/ lead existente
- `templates/tenants/scan_success.html`
- `migrations/` — criadas para `accounts` e `tenants`
- `static/` — pasta criada (vazia por ora)

**Motivo:**
Construção inicial do sistema conforme prompt determinístico do MVP.

**Impacto:**
Sistema completo e funcional. Servidor Django rodando na porta 8000.

---

## 📌 Estado Atual

### ✅ Funcionando
- Login único com redirecionamento por papel (`is_admin`)
- Admin Dashboard: lista de tenants com métricas (leads, visitas, valor total via `annotate`)
- CRUD de Tenants (criar com usuário vinculado, editar, excluir)
- Cliente Dashboard: widgets para gerar QR fixo e com valor
- Geração de QR Code dinâmica (sem salvar no banco), exibição em base64 inline
- Página de Scan (`/scan/<tenant_id>/`):
  - Lead novo → exibe formulário completo
  - Lead existente (mesmo telefone+tenant) → exibe botão de confirmação
  - Sempre registra uma `Visit` com valor opcional
- Página de sucesso pós-scan com mensagem contextual
- Superuser `admin` / `admin123` criado com `is_admin=True`

### ⚠️ Observações de segurança (apenas para prod)
- `DEBUG=True` — manter em dev, alterar para prod
- `SECRET_KEY` deve ser trocada em produção
- HTTPS/HSTS não configurado (esperado para MVP local)

### 🔧 O que ainda não existe
- Paginação nas listagens
- Filtro de datas no dashboard
- Export de leads (CSV etc.)
- Deploy / WSGI de produção

---

## 🚧 Próximos Passos

1. Adicionar paginação à lista de tenants e leads
2. Adicionar filtros de data nas métricas do dashboard
3. Implementar export CSV de leads por tenant
4. Configurar variáveis de ambiente (`.env`) para prod
5. Dockerizar o projeto

---

## ⚠️ Observações Importantes

- **AUTH_USER_MODEL = 'accounts.User'** — nunca reverter para o User padrão do Django após migrations aplicadas
- **QR Code gerado em memória** (base64) — nunca salvo no banco, conforme especificação
- **Identificador único do lead:** `phone` + `tenant` (via `get_or_create`)
- **Tenant criado junto com usuário** no mesmo form — lógica na view `tenant_create`
- **`is_admin` ≠ `is_staff`** — `is_admin` controla o fluxo da aplicação; `is_staff` controla acesso ao `/django-admin/`

---

## 🔑 Credenciais de Desenvolvimento

| Usuário | Senha     | Papel |
|---------|-----------|-------|
| admin   | admin123  | Admin (is_admin=True, is_staff=True, is_superuser=True) |

---

## 🌐 Rotas do Sistema

| Rota | Descrição |
|------|-----------|
| `/login` | Tela de login única |
| `/logout` | Logout |
| `/admin-dashboard` | Dashboard administrativo com métricas |
| `/admin/tenants` | Lista de tenants |
| `/admin/tenants/criar` | Criar tenant + usuário |
| `/admin/tenants/<id>/editar` | Editar tenant |
| `/admin/tenants/<id>/excluir` | Excluir tenant |
| `/cliente-dashboard` | Painel do cliente com links de QR |
| `/gerar-qr` | Gera QR Code (aceita `?valor=XX.XX`) |
| `/scan/<tenant_id>/` | Captura lead e registra visita |
| `/django-admin/` | Admin nativo do Django |
