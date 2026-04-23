# PROMPT — Geração de MVP QR Code Multi-Tenant (Determinístico)

## 🎯 OBJETIVO

Gerar um sistema MVP completo, funcional e consistente de captura de leads via QR Code com arquitetura multi-tenant.

O sistema deve conter:

* Autenticação única
* Separação de perfis (Admin e Cliente)
* Geração de QR Code
* Captura e identificação de leads
* Dashboard administrativo com métricas

Este prompt é **determinístico**. Siga rigorosamente cada instrução sem improvisações, sem adicionar features extras e sem alterar a arquitetura.

---

## ⚙️ STACK OBRIGATÓRIA

* Backend: Django
* Banco de Dados: Sqlite (por enquanto)
* ORM: Django ORM
* Frontend: Django Templates (NÃO usar React)
* QR Code: biblioteca `qrcode` (Python)
* Autenticação: sistema padrão do Django

---

## 🧱 ESTRUTURA DO PROJETO

Crie um projeto Django com:

* App principal: `core`
* App de autenticação/usuário: `accounts`
* App de negócio: `tenants`

---

## 🧩 MODELOS (OBRIGATÓRIOS)

Implemente exatamente estes modelos:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    cohort = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, null=True, blank=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class Lead(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Visit(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔐 AUTENTICAÇÃO

* Criar tela única `/login`
* Após login:

```python
if user.is_admin:
    redirect('/admin-dashboard')
else:
    redirect('/cliente-dashboard')
```

---

## 👨‍💼 ÁREA ADMIN

### Rota:

`/admin-dashboard`

### Funcionalidades obrigatórias:

1. Dashboard com:

   * Total de tenants
   * Total de leads por tenant
   * Total de visitas por tenant
   * Valor total capturado (somatório de Visit.value)

2. CRUD de tenants:

   * Nome
   * Cohort
   * Criar usuário vinculado ao tenant
   * Definir senha manualmente

---

## 🧑‍💻 ÁREA CLIENTE

### Rota:

`/cliente-dashboard`

### Funcionalidades:

#### 1. Gerar QR Code FIXO

URL:

```
/scan/<tenant_id>/
```

#### 2. Gerar QR Code COM VALOR

URL:

```
/scan/<tenant_id>/?valor=XX.XX
```

* O QR Code deve ser exibido na tela
* Não salvar QR no banco (geração dinâmica)

---

## 📲 PÁGINA DE SCAN

### Rota:

```
/scan/<tenant_id>/
```

### Lógica obrigatória:

1. Capturar parâmetro `valor` da URL (opcional)

2. Identificação do lead:

* Usar telefone como identificador único

* Se telefone NÃO existir:

  * Mostrar formulário:

    * Nome
    * Telefone
    * Data de nascimento
  * Criar Lead

* Se telefone JÁ existir:

  * NÃO pedir dados novamente

3. Sempre registrar uma visita:

```python
Visit.objects.create(
    lead=lead,
    tenant=tenant,
    value=valor (se existir)
)
```

---

## 🔁 FLUXO COMPLETO

1. Admin cria tenant + usuário
2. Cliente loga
3. Cliente gera QR Code
4. Lead escaneia QR
5. Lead:

   * Se novo → cadastra
   * Se existente → reconhecido
6. Sistema registra visita
7. Admin visualiza métricas

---

## 📊 MÉTRICAS OBRIGATÓRIAS

No dashboard admin, calcular:

* Leads por tenant
* Visitas por tenant
* Total de visitas
* Valor total capturado (SUM de Visit.value)

---

## 🌐 ROTAS OBRIGATÓRIAS

```
/login
/admin-dashboard
/admin/tenants
/cliente-dashboard
/gerar-qr
/scan/<tenant_id>/
```

---

## 🎨 INTERFACE

* Usar Django Templates
* Layout simples (HTML + Bootstrap opcional)
* Não usar frameworks JS complexos

---

## 🚫 RESTRIÇÕES (CRÍTICO)

* NÃO usar React
* NÃO usar microservices
* NÃO usar autenticação externa
* NÃO criar features adicionais
* NÃO modificar os modelos definidos
* NÃO alterar o fluxo

---

## ✅ RESULTADO ESPERADO

O sistema deve permitir:

* Admin gerenciar clientes
* Cliente gerar QR Codes
* Leads se cadastrarem via QR
* Sistema registrar visitas automaticamente
* Dashboard com métricas claras

---

## 🔚 FIM DO PROMPT

Gerar o projeto completo com:

* Models
* Views
* URLs
* Templates básicos
* Lógica funcional completa

Sem explicações. Apenas código organizado.
