# RevEngine — Arquitetura Técnica (MVP)

## 🧱 Stack Tecnológica

* Backend: Django
* Banco: PostgreSQL
* Assíncrono: Celery + Redis
* Comunicação: WhatsApp API (Z-API / Twilio)
* Frontend: HTML simples / Django Templates
* Hospedagem: VPS (DigitalOcean / AWS)

---

## 🗂️ Estrutura do Projeto

```
revengine/
├── core/
├── customers/
├── visits/
├── campaigns/
├── referrals/
├── automation/
├── integrations/
└── api/
```

---

## 🧬 Modelos de Banco (Essenciais)

### 👤 Customer

```python
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    total_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)

    segment = models.CharField(max_length=20, default='new')
```

---

### 📍 Visit

```python
class Visit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    source = models.CharField(max_length=50)  # QR, referral, manual
```

---

### 🎯 Campaign

```python
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    trigger_type = models.CharField(max_length=50)  # D+3, birthday, inactivity
    active = models.BooleanField(default=True)
```

---

### 🔁 Referral

```python
class Referral(models.Model):
    referrer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='referrer')
    referred = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='referred')
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔄 Fluxo de Automação

### 🆕 Novo Cliente

1. Cliente se cadastra via QR
2. Sistema cria `Customer`
3. Dispara:

* WhatsApp D+0 (boas-vindas)
* Agenda próximos eventos

---

### ⏱️ Engine de Tempo (Celery)

Exemplo:

```python
@shared_task
def send_d3_message(customer_id):
    # lógica de envio
```

---

### 📅 Regras de Automação

| Evento      | Ação               |
| ----------- | ------------------ |
| D+0         | WhatsApp Welcome   |
| D+3         | Oferta             |
| D+7         | Storytelling       |
| D+14        | Tentativa final    |
| 21 dias     | Alerta inatividade |
| Aniversário | Promoção           |

---

## 🧠 Segmentação Automática

Rodar diariamente:

```python
def update_segments():
    for customer in Customer.objects.all():
        days = (now() - customer.last_visit).days

        if days <= 30:
            customer.segment = 'champion'
        elif days <= 60:
            customer.segment = 'at_risk'
        else:
            customer.segment = 'lost'
```

---

## 🔗 Sistema de Referral

### Geração de link

```
https://app.com/register?ref=ABC123
```

### Lógica:

* ao cadastrar → vincula referrer
* gera recompensa

---

## 📲 Integração com WhatsApp

Abstração:

```python
def send_whatsapp(phone, message):
    # integração API externa
```

---

## 📊 Tracking de Eventos

Criar tabela opcional:

```python
class EventLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## ⚡ Endpoint de Captura (QR)

```python
POST /api/register
```

Payload:

```json
{
  "name": "Gabriel",
  "phone": "31999999999",
  "ref": "ABC123"
}
```

---

## 🔐 Segurança

* validação de telefone
* rate limit
* opt-in LGPD (checkbox)

---

## 🚀 Roadmap Técnico (MVP → Escala)

### MVP (Semana 1)

* cadastro
* envio WhatsApp
* tracking básico

### V1

* segmentação automática
* referral funcional

### V2

* dashboard
* múltiplos clientes (multi-tenant)

### V3

* IA voice
* integrações com PDV

---

## 🧩 Futuro (Escalabilidade)

* microservices
* fila distribuída
* data warehouse

---

## 📌 Conclusão

Arquitetura simples, desacoplada e escalável.

Foco:

> velocidade de validação, não perfeição técnica
