# 🛡️ Como Funciona a Análise STRIDE

## Visão Geral

O código STRIDE (`gerar_stride_completo.py`) funciona em **2 camadas**:

1. **Ameaças Base**: Por tipo de componente (isolado)
2. **Ameaças Contextuais**: Por conexão entre componentes (fluxo)

---

## 1️⃣ Ameaças Base (Por Componente)

### Como Funciona

```python
# Mapeamento: Tipo de Componente → Ameaças STRIDE
STRIDE_RULES = {
    "user": ["Spoofing", "Repudiation"],
    "api": ["Spoofing", "Tampering", "DoS", "Elevation of Privilege"],
    "database": ["Tampering", "Information Disclosure", "Repudiation"],
    "storage": ["Information Disclosure", "Tampering"],
}
```

### Exemplo Prático

**Input**: Componente detectado
```json
{
  "label": "aws_rds",
  "prob": 0.85
}
```

**Processamento**:
1. Normaliza label: `aws_rds` → tipo `database`
2. Busca ameaças: `database` → `["Tampering", "Information Disclosure", "Repudiation"]`
3. Adiciona contramedidas para cada ameaça

**Output**: Ameaças base
```json
{
  "component": "aws_rds",
  "component_type": "database",
  "stride": "Tampering",
  "severity": "MEDIUM",
  "description": "Tampering em aws_rds",
  "mitigations": ["TLS", "Validação de entrada", "Integridade de dados"]
}
```

### Mapeamento de Labels

```python
TAG_TO_TYPE = {
    "AWS_RDS": "database",
    "AWS_DYNAMODB": "database",
    "AZURE_SQL": "database",
    "GCP_CLOUD_SQL": "database",
    
    "AWS_APPLICATION_LOAD_BALANCER": "lb",
    "AZURE_LOAD_BALANCERS": "lb",
    
    "USER": "user",
    # ... 111 classes mapeadas
}
```

**Por que isso é importante?**
- Labels específicos (aws_rds) → Tipo genérico (database)
- Permite aplicar regras STRIDE consistentes
- Funciona com AWS, Azure e GCP

---

## 2️⃣ Ameaças Contextuais (Por Conexão)

### Como Funciona

Analisa o **fluxo de dados** entre componentes:

```python
def generate_contextual_threats(connections):
    for conn in connections:
        source = conn["from"]  # Origem
        target = conn["to"]    # Destino
        
        source_type = tag_to_type(source)
        target_type = tag_to_type(target)
        
        # Regras contextuais
        if source_type == "user" and target_type == "database":
            # CRÍTICO: Usuário acessando banco direto!
            threats.append({
                "stride": "Elevation of Privilege",
                "severity": "CRITICAL",
                "description": "Acesso direto de usuário ao banco sem camada intermediária"
            })
```

### Regras Implementadas

#### Regra 1: USER → DATABASE (CRÍTICO)
```python
if source_type == "user" and target_type == "database":
    # 🔴 CRITICAL
    # Usuário não deveria acessar banco direto
    # Deve ter API/camada intermediária
```

**Por quê?**
- Expõe banco diretamente
- Sem validação de negócio
- Risco de SQL injection
- Sem auditoria adequada

#### Regra 2: USER → API (sem WAF)
```python
if source_type == "user" and target_type in ["api", "lb"]:
    has_waf = any(c["from"] == "security" for c in connections)
    
    if not has_waf:
        # 🟠 HIGH
        # Exposição externa sem proteção
```

**Por quê?**
- API exposta sem WAF
- Vulnerável a DDoS
- Sem rate limiting
- Sem proteção contra OWASP Top 10

#### Regra 3: API → DATABASE
```python
if source_type == "api" and target_type == "database":
    # 🟠 HIGH
    # Risco de SQL Injection
    # Conexão deve ser criptografada
```

**Por quê?**
- Entrada não validada pode causar SQL injection
- Conexão deve usar TLS
- Credenciais devem estar em vault

#### Regra 4: Qualquer Conexão
```python
# Para TODA conexão detectada
threats.append({
    "stride": "Information Disclosure",
    "severity": "MEDIUM",
    "description": f"Garantir criptografia em trânsito entre {source} e {target}"
})
```

**Por quê?**
- Dados em trânsito devem ser criptografados
- TLS 1.3 mínimo
- mTLS quando aplicável

---

## 🎯 Exemplo Completo

### Input: Diagrama Detectado

**Componentes**:
```json
[
  {"label": "user", "prob": 0.92},
  {"label": "aws_application_load_balancer", "prob": 0.85},
  {"label": "aws_rds", "prob": 0.88}
]
```

**Conexões**:
```json
[
  {"from": "user", "to": "aws_application_load_balancer", "confidence": 0.75},
  {"from": "aws_application_load_balancer", "to": "aws_rds", "confidence": 0.82}
]
```

### Processamento

#### Etapa 1: Ameaças Base

**user** (tipo: user)
- ✅ Spoofing
- ✅ Repudiation

**aws_application_load_balancer** (tipo: lb)
- ✅ Denial of Service
- ✅ Tampering

**aws_rds** (tipo: database)
- ✅ Tampering
- ✅ Information Disclosure
- ✅ Repudiation

**Total**: 7 ameaças base

#### Etapa 2: Ameaças Contextuais

**Conexão 1**: user → aws_application_load_balancer
- Verifica se tem WAF no caminho
- Se não tem: 🟠 HIGH - "Conexão externa sem WAF"

**Conexão 2**: aws_application_load_balancer → aws_rds
- 🟠 HIGH - "Risco de SQL Injection"
- 🟡 MEDIUM - "Garantir criptografia em trânsito"

**Total**: 3 ameaças contextuais

### Output: Relatório STRIDE

```markdown
## 📊 Diagrama: imagem_1.png

### Resumo
- Componentes: 3
- Conexões: 2
- Ameaças base: 7
- Ameaças contextuais: 3

### 🔄 Fluxo de Dados
- user → aws_application_load_balancer
- aws_application_load_balancer → aws_rds

### 🛡️ Análise STRIDE

#### Spoofing (1 ameaça)
🟡 MEDIUM: Spoofing em user
   - Contramedidas: MFA, OAuth2/OIDC

#### Tampering (3 ameaças)
🟠 HIGH [CONTEXTUAL]: Risco de SQL Injection na conexão API-Database
   - Componente: aws_application_load_balancer → aws_rds
   - Contramedidas: Prepared statements, ORM, Validação de entrada

🟡 MEDIUM: Tampering em aws_application_load_balancer
🟡 MEDIUM: Tampering em aws_rds

#### Information Disclosure (3 ameaças)
🟡 MEDIUM [CONTEXTUAL]: Garantir criptografia em trânsito
🟡 MEDIUM: Information Disclosure em aws_rds
```

---

## 🎨 Para a Apresentação

### Slide 1: Visão Geral

```
┌─────────────────────────────────────────┐
│  Componentes Detectados                 │
│  ↓                                       │
│  Ameaças Base (por tipo)                │
│  +                                       │
│  Conexões Detectadas                    │
│  ↓                                       │
│  Ameaças Contextuais (por fluxo)        │
│  =                                       │
│  Relatório STRIDE Completo              │
└─────────────────────────────────────────┘
```

### Slide 2: Ameaças Base

**Conceito**: "O que pode dar errado com ESTE componente?"

**Exemplo**:
- DATABASE → Tampering, Information Disclosure
- API → Spoofing, DoS, Elevation of Privilege
- USER → Spoofing, Repudiation

**Código**:
```python
# Simples: Tipo → Ameaças
STRIDE_RULES = {
    "database": ["Tampering", "Information Disclosure"],
    "api": ["Spoofing", "DoS", "Elevation of Privilege"]
}
```

### Slide 3: Ameaças Contextuais

**Conceito**: "O que pode dar errado com ESTA conexão?"

**Exemplo**:
- USER → DATABASE: 🔴 CRITICAL (não deveria existir!)
- USER → API (sem WAF): 🟠 HIGH (exposto sem proteção)
- API → DATABASE: 🟠 HIGH (risco de SQL injection)

**Código**:
```python
# Analisa o fluxo
if source == "user" and target == "database":
    # CRÍTICO: Acesso direto!
    severity = "CRITICAL"
```

### Slide 4: Diferencial

**Antes (só componentes)**:
- 7 ameaças genéricas
- Não vê problemas de arquitetura

**Depois (componentes + conexões)**:
- 7 ameaças base + 3 contextuais
- Detecta: USER → DATABASE direto
- Detecta: API sem WAF
- Detecta: Conexões sem criptografia

**Ganho**: +43% mais ameaças detectadas

---

## 💡 Pontos-Chave para Apresentar

### 1. Duas Camadas de Análise

"Não basta saber QUE componentes existem. Precisamos saber COMO eles se conectam."

### 2. Ameaças Contextuais são o Diferencial

"Um banco de dados isolado tem ameaças. Mas um banco acessado diretamente por usuários? Isso é CRÍTICO."

### 3. Baseado em Best Practices

"As regras não são inventadas. São baseadas em OWASP, STRIDE da Microsoft, e padrões de arquitetura segura."

### 4. Escalável

"Hoje temos 4 regras contextuais. Amanhã podemos ter 40. O framework está pronto."

---

## 📊 Métricas de Impacto

### Sem Análise de Fluxo
- Ameaças detectadas: 7
- Ameaças críticas: 0
- Problemas arquiteturais: Não detectados

### Com Análise de Fluxo
- Ameaças detectadas: 10 (+43%)
- Ameaças críticas: Possível (USER → DB)
- Problemas arquiteturais: Detectados

---

## 🎬 Script para Demo

**[Mostrar código]**

"Aqui está o coração do sistema. Primeiro, mapeamos cada componente para um tipo genérico. AWS RDS, Azure SQL, GCP Cloud SQL - todos viram 'database'."

**[Mostrar STRIDE_RULES]**

"Então aplicamos as regras STRIDE. Database tem Tampering e Information Disclosure. API tem Spoofing e DoS."

**[Mostrar generate_contextual_threats]**

"Mas o diferencial está aqui. Analisamos as CONEXÕES. Se vemos USER conectando direto com DATABASE, isso é CRÍTICO. Não deveria existir."

**[Mostrar relatório]**

"E o resultado? Um relatório completo com ameaças base E contextuais. Não só 'seu banco pode ser adulterado', mas 'seu usuário está acessando o banco direto - adicione uma API no meio'."

---

## 🔑 Mensagem Final

"A inovação não é só detectar componentes. É entender o FLUXO entre eles e gerar ameaças baseadas em como o sistema realmente funciona."
