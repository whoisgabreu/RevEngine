# 🚀 RevEngine MVP — Guia Completo de Implementação (Django + Celery)

## 📦 1. Pré-requisitos

- Python 3.10+
- pip
- virtualenv
- Redis
- PostgreSQL

---

## 🏗️ 2. Criar Projeto

```bash
mkdir revengine
cd revengine

python -m venv venv
source venv/bin/activate  # Linux
# venv\Scripts\activate   # Windows

pip install django djangorestframework psycopg2-binary celery redis python-dotenv
```

---

## ⚙️ 3. Iniciar Django

```bash
django-admin startproject config .
python manage.py startapp customers
python manage.py startapp visits
python manage.py startapp campaigns
python manage.py startapp referrals
python manage.py startapp automation
python manage.py startapp api
```

---

## 🧩 4. Configuração do settings.py

```python
INSTALLED_APPS = [
    'rest_framework',
    'customers',
    'visits',
    'campaigns',
    'referrals',
    'automation',
    'api',
]
```

---

## 🐘 5. Configurar PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'revengine',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🧬 6. Models

### Customer
```python
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    birthday = models.DateField(null=True, blank=True)
    total_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)
    segment = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔄 7. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🌐 8. API de Cadastro

```python
@api_view(['POST'])
def register(request):
    name = request.data.get('name')
    phone = request.data.get('phone')

    customer, created = Customer.objects.get_or_create(
        phone=phone,
        defaults={'name': name}
    )

    return Response({"status": "ok", "created": created})
```

---

## 📲 9. WhatsApp Mock

```python
def send_whatsapp(phone, message):
    print(f"Sending to {phone}: {message}")
```

---

## ⚡ 10. Celery

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
```

---

## ⏱️ 11. Tasks

```python
@shared_task
def send_welcome(customer_id):
    ...

@shared_task
def send_d3(customer_id):
    ...
```

---

## 🔁 12. Automação no Cadastro

```python
if created:
    send_welcome.delay(customer.id)
    send_d3.apply_async((customer.id,), countdown=3*24*60*60)
```

---

## 🧪 13. Rodar

```bash
python manage.py runserver
celery -A config worker -l info
redis-server
```

---

## 🔗 14. Teste

```bash
curl -X POST http://127.0.0.1:8000/api/register/
```

---

# 🎯 17. Próximos Passos

Depois que isso estiver rodando:

- Criar landing page com QR Code
- Implementar sistema de referral (links únicos)
- Integrar WhatsApp real (API oficial ou provedores)
- Criar dashboard básico (KPIs)
- Implementar multi-tenant (vários clientes/empresas)
- Adicionar autenticação e painel admin customizado
- Criar sistema de campanhas dinâmicas
- Implementar triggers (aniversário, inatividade, etc.)
- Deploy em VPS (Docker + Nginx recomendado)

---

# 🏁 Conclusão

Você agora tem a base do RevEngine funcionando:

- Captura de clientes
- CRM inicial
- Automação
- Base escalável

Próximo nível: transformar isso em produto vendável.
