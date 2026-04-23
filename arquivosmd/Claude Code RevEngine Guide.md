# 🧠 RevEngine — Agent Build Guide (Para Code Assistants)

## 🎯 OBJECTIVE

Você é um agente de engenharia responsável por construir um sistema chamado **RevEngine**.

O objetivo do sistema é:

> Criar um motor de crescimento de receita para negócios físicos, focado em captura de clientes, automação de relacionamento e geração de indicações.

O sistema NÃO depende de integração com PDVs.

---

# ⚠️ CORE PRINCIPLE

NUNCA dependa de integração com sistemas externos de PDV.

O sistema deve funcionar de forma **independente**, usando:

* QR Code
* Formulários
* Links de indicação
* WhatsApp como identificador

---

# 🧱 SYSTEM ARCHITECTURE

## Stack obrigatória:

* Backend: Django
* API: Django REST Framework
* Banco: PostgreSQL
* Assíncrono: Celery + Redis

---

# 📦 MODULES (APPS DJANGO)

Crie os seguintes apps:

* customers
* visits
* campaigns
* referrals
* automation
* api

---

# 🧬 DATA MODELS

## Customer

Campos obrigatórios:

* id
* name
* phone (único, chave principal)
* birthday (opcional)
* total_visits
* last_visit
* segment (new, champion, at_risk, lost)
* created_at

---

## Visit

* customer (FK)
* created_at
* source (qr, referral, manual)

---

## Campaign

* name
* message
* trigger_type (D+3, birthday, inactivity)
* active

---

## Referral

* referrer (FK Customer)
* referred (FK Customer)
* created_at

---

## (Opcional) EventLog

* customer
* event_type
* created_at

---

# 🔄 CORE FLOWS

## 1. CUSTOMER REGISTRATION

Trigger: POST /api/register

Entrada:

```json
{
  "name": "string",
  "phone": "string",
  "ref": "optional"
}
```

Lógica:

1. Criar ou recuperar Customer pelo telefone
2. Se novo:

   * salvar
   * registrar referral (se houver)
   * disparar automações

---

## 2. AUTOMATION ENGINE

Após cadastro:

* D+0 → mensagem de boas-vindas
* D+3 → oferta
* D+7 → branding/story
* D+14 → última tentativa

Se não houver resposta:

* pausar 45 dias
* reiniciar ciclo

---

## 3. SEGMENTATION

Rodar diariamente:

* champion: visita <= 30 dias
* at_risk: 31–60 dias
* lost: > 60 dias

---

## 4. REFERRAL SYSTEM

* gerar código único por cliente
* criar link:

```
/register?ref=CODE
```

* vincular novos clientes ao referrer
* preparar lógica de recompensa

---

## 5. VISIT TRACKING

Criar endpoint:

POST /api/visit

Função:

* registrar visita
* atualizar last_visit
* incrementar total_visits

---

# 📲 WHATSAPP INTEGRATION

Criar função abstrata:

```python
def send_whatsapp(phone, message):
    pass
```

Inicialmente simular com print/log.

Deixar pronto para futura integração com API externa.

---

# ⏱️ ASYNC TASKS (CELERY)

Criar tarefas:

* send_welcome
* send_d3
* send_d7
* send_d14

Usar:

* delay()
* apply_async(countdown=...)

---

# 🔐 VALIDATIONS

* telefone obrigatório e único
* evitar duplicidade
* tratar concorrência

---

# 🌐 API ENDPOINTS

Criar endpoints:

* POST /api/register
* POST /api/visit
* GET /api/customer/<id>
* GET /api/referral/<code>

---

# 📊 NON-GOALS (NÃO IMPLEMENTAR AGORA)

* dashboards complexos
* IA de voz
* integrações com PDV
* multi-tenant avançado

---

# 🧪 MVP REQUIREMENTS

O sistema é considerado funcional quando:

* cadastro via API funciona
* automações são disparadas
* referrals são registrados
* visitas são rastreadas
* segmentação roda corretamente

---

# 🧭 EXECUTION PLAN

## PASSO 1

Criar projeto Django + apps

## PASSO 2

Implementar models

## PASSO 3

Rodar migrations

## PASSO 4

Criar API de registro

## PASSO 5

Implementar Celery

## PASSO 6

Criar tarefas automáticas

## PASSO 7

Implementar referral

## PASSO 8

Implementar tracking de visitas

## PASSO 9

Testar fluxo completo

---

# 🧠 BEHAVIOR RULES (IMPORTANT)

Você deve:

* escrever código limpo e modular
* evitar overengineering
* priorizar funcionamento rápido
* documentar funções principais
* usar nomes claros

Você NÃO deve:

* adicionar features fora do escopo
* integrar sistemas externos desnecessários
* complicar arquitetura no MVP

---

# 🏁 FINAL GOAL

Entregar um sistema que permita:

1. Capturar clientes via QR/API
2. Disparar automações automaticamente
3. Rastrear visitas
4. Gerar crescimento via indicação

---

# 🔥 SUCCESS CRITERIA

Se um negócio conseguir:

* cadastrar clientes
* enviar mensagens automáticas
* trazer clientes de volta
* gerar novas indicações

Então o sistema está correto.

---

# 🚀 NEXT EVOLUTION (FUTURE)

Após MVP:

* multi-tenant
* dashboard
* IA voice
* integrações com PDV
* engine de campanhas avançado

---

# 📌 FINAL INSTRUCTION

Comece implementando o projeto completo seguindo este documento.

Priorize funcionamento sobre perfeição.
