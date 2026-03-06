# Projeto de Modelagem de Ameaças com IA + STRIDE

Este projeto usa dois modelos YOLO para analisar diagramas de arquitetura: um detecta componentes (ícones) e outro detecta conexões (setas). A análise integrada gera um relatório STRIDE completo com ameaças base e contextuais baseadas no fluxo de dados.

## Funcionalidades

- ✅ **Dupla detecção**: Componentes (best_icons.pt) + Setas (best_arrows.pt)
- ✅ **Mapeamento de fluxo**: Identifica origem e destino de cada conexão
- ✅ **STRIDE integrado**: Ameaças base (por componente) + contextuais (por conexão)
- ✅ **Ameaças críticas**: Detecta padrões perigosos (ex: USER → DATABASE direto)
- ✅ **Análise completa**: 111 classes de componentes AWS/Azure/GCP

## Pre-requisitos

- Python 3.10+
- Modelos YOLO treinados em `models/`:
  - `best_icons.pt` (18MB) - Detecta 111 tipos de componentes
  - `best_arrows.pt` (19MB) - Detecta setas/conexões

## Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

## Uso Rápido

### Pipeline Completo (Recomendado)

Execute o orquestrador que roda todas as etapas e versiona os resultados:

```bash
# macOS/Linux (use caminho direto do venv para evitar conflitos com aliases)
.venv/bin/python analise_stride.py --icons-threshold 0.6 --arrows-threshold 0.4 --device mps

# Windows
.venv\Scripts\python analise_stride.py --icons-threshold 0.6 --arrows-threshold 0.4 --device cpu

# Ou se o venv estiver ativado corretamente (sem aliases conflitantes)
python analise_stride.py --icons-threshold 0.6 --arrows-threshold 0.4 --device cpu
```

**Dispositivos disponíveis:**
- `cpu` - Funciona em qualquer sistema
- `mps` - Aceleração GPU em Mac M1/M2/M3
- `cuda` - Aceleração GPU NVIDIA

**O que o pipeline faz:**
1. Cria pasta versionada `outputs/run_TIMESTAMP/` com todos os resultados
2. **Detecção de componentes** (best_icons.pt)
3. **Detecção de setas** (best_arrows.pt)
4. **Mapeamento de conexões** (seta → componentes)
5. **Geração STRIDE completa** (base + contextual)

**Resultados:** Todos os arquivos ficam em `outputs/run_TIMESTAMP/`:
- `predictions_yolo.json` - Componentes detectados
- `arrows_detected.json` - Setas detectadas
- `connections.json` - Conexões mapeadas
- `stride_completo.md` - Relatório STRIDE
- `threat_model_completo.json` - Modelo de ameaças JSON

### Opções Avançadas

```bash
# Usar pasta de output customizada
.venv/bin/python analise_stride.py --output-dir outputs/minha_analise

# Pular etapas (útil para re-gerar apenas o STRIDE)
.venv/bin/python analise_stride.py --only-stride

# Ajustar thresholds
.venv/bin/python analise_stride.py --icons-threshold 0.7 --arrows-threshold 0.3

# Ver todas as opções
.venv/bin/python analise_stride.py --help
```

## Como Funciona

O pipeline é executado automaticamente pelo `analise_stride.py`, mas você também pode rodar cada etapa individualmente:

### 1. Detecção de Componentes (best_icons.pt)

```bash
.venv/bin/python scripts/detectar_componentes_yolo.py \
    --model models/best_icons.pt \
    --input imagens_validacao \
    --threshold 0.6 \
    --device cpu
```

**Detecta**: API Gateway, Database, Load Balancer, VPC, Subnets, etc.
**Saída**: JSON com componentes detectados

### 2. Detecção de Setas (best_arrows.pt)

```bash
.venv/bin/python scripts/detectar_setas_yolo.py \
    --model models/best_arrows.pt \
    --components <caminho_do_json_componentes> \
    --threshold 0.4 \
    --device cpu
```

**Detecta**: Setas/linhas de conexão
**Mapeia**: Qual componente conecta com qual
**Saída**: JSON com conexões mapeadas

### 3. Análise STRIDE Integrada

```bash
.venv/bin/python scripts/gerar_stride_completo.py \
    --components <caminho_do_json_componentes> \
    --connections <caminho_do_json_conexoes>
```

**Gera**:
- Ameaças base (por tipo de componente)
- Ameaças contextuais (por conexão)
- Detecção de padrões críticos

**Exemplo de ameaça contextual**:
```
🔴 CRITICAL: Acesso direto de usuário ao banco de dados
   Conexão: USER → DATABASE
   Contramedidas: Adicionar API Gateway, Implementar camada de aplicação
```

## Estrutura de Saídas

Cada execução cria uma pasta versionada com timestamp:

```
outputs/
├── run_2026_03_06_112153/           # Pasta versionada por execução
│   ├── predictions_yolo.json        # Componentes detectados
│   ├── arrows_detected.json         # Setas detectadas
│   ├── connections.json             # Conexões mapeadas (origem → destino)
│   ├── threat_model_completo.json   # Ameaças base + contextuais (JSON)
│   └── stride_completo.md           # Relatório STRIDE integrado (Markdown)
├── run_2026_03_06_143022/           # Outra execução
│   └── ...
└── run_2026_03_07_091500/           # Mais uma execução
    └── ...
```

**Vantagens do versionamento:**
- Histórico completo de todas as análises
- Comparação entre diferentes execuções
- Nenhum resultado é sobrescrito
- Fácil rastreabilidade




## Modelos YOLO

### best_icons.pt (18MB)
- **Classes**: 111 tipos de componentes
- **Clouds**: AWS, Azure, GCP
- **Exemplos**: API Gateway, RDS, Lambda, VPC, Load Balancer, etc.

### best_arrows.pt (19MB)
- **Função**: Detecta setas/linhas de conexão
- **Uso**: Mapeia fluxo de dados entre componentes

## Tipos de Ameaças

### Ameaças Base (por componente)
Geradas automaticamente baseado no tipo:
- **USER**: Spoofing, Repudiation
- **API**: Spoofing, Tampering, DoS, Elevation of Privilege
- **DATABASE**: Tampering, Information Disclosure, Repudiation
- **STORAGE**: Information Disclosure, Tampering

### Ameaças Contextuais (por conexão)
Detectadas pela análise de fluxo:
- **USER → DATABASE**: 🔴 CRITICAL - Acesso direto sem camada intermediária
- **USER → API (sem WAF)**: 🟠 HIGH - Exposição sem proteção
- **API → DATABASE**: 🟠 HIGH - Risco de SQL Injection
- **Qualquer conexão**: 🟡 MEDIUM - Garantir criptografia em trânsito

## Exemplo de Resultado

Para um diagrama com USER → API → DATABASE:

```markdown
### 🚨 AMEAÇAS CRÍTICAS
#### Elevation of Privilege: Acesso direto de usuário ao banco de dados
**Componente**: USER → DATABASE
**Contramedidas**:
- Adicionar API Gateway
- Implementar camada de aplicação
- Remover acesso direto

### 🛡️ Análise STRIDE Completa
#### Information Disclosure (5 ameaças)
🟠 HIGH [CONTEXTUAL]: Risco de SQL Injection na conexão API-Database
   - Componente: API → DATABASE
   - Contramedidas: Prepared statements, ORM, Validação de entrada
```

## Licença

Projeto desenvolvido para o Hackathon FIAP Software Security.
