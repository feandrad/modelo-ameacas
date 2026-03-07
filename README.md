# Projeto de Modelagem de Ameaças com IA + STRIDE

Este projeto usa dois modelos YOLO para analisar diagramas de arquitetura: um detecta componentes (ícones) e outro detecta conexões (setas). A análise integrada gera um relatório STRIDE completo com ameaças base e contextuais baseadas no fluxo de dados.

## Datasets
- **Arrows**: https://universe.roboflow.com/arrowhead-yjeny/arrow-dataset-ijzxx/dataset/1
- **Icons**: https://www.kaggle.com/datasets/carlosrian/software-architecture-dataset/code

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

### Pipeline Completo com Visualização (Recomendado)

Execute o pipeline que detecta componentes, setas e gera visualizações:

```bash
# Executar pipeline completo
python scripts/pipeline_completo.py --input imagens_validacao --device cpu

# Com thresholds customizados
python scripts/pipeline_completo.py \
    --input imagens_validacao \
    --threshold-components 0.6 \
    --threshold-arrows 0.4 \
    --device mps
```

**O que o pipeline faz:**
1. **Detecta componentes** com best_icons.pt
2. **Detecta setas** com best_arrows.pt
3. **Gera visualizações** com boxes e arrows desenhadas

**Resultados:**
- `data/predictions/predictions_yolo.json` - Componentes detectados
- `data/arrows_output/arrows_detected.json` - Setas detectadas
- `data/arrows_output/connections.json` - Conexões mapeadas
- `outputs/visualizacoes/` - **Imagens com detecções desenhadas** ✨

### Pipeline STRIDE Completo

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
6. **Geração de visualizações** (imagens com boxes e arrows) ✨

**Resultados:** Todos os arquivos ficam em `outputs/run_TIMESTAMP/`:
- `predictions_yolo.json` - Componentes detectados
- `arrows_detected.json` - Setas detectadas
- `connections.json` - Conexões mapeadas
- `stride_completo.md` - Relatório STRIDE
- `threat_model_completo.json` - Modelo de ameaças JSON
- `visualizacoes/` - **Imagens com detecções desenhadas** ✨

### Opções Avançadas

```bash
# Usar pasta de output customizada
.venv/bin/python analise_stride.py --output-dir outputs/minha_analise

# Pular etapas (útil para re-gerar apenas o STRIDE)
.venv/bin/python analise_stride.py --only-stride

# Pular visualizações (mais rápido se não precisar das imagens)
.venv/bin/python analise_stride.py --skip-visualizations

# Ajustar thresholds
.venv/bin/python analise_stride.py --icons-threshold 0.7 --arrows-threshold 0.3

# Ver todas as opções
.venv/bin/python analise_stride.py --help
```

## Como Funciona

### Visualização das Detecções

Para gerar apenas as visualizações (se já tem os JSONs):

```bash
python scripts/visualizar_deteccoes.py \
    --components data/predictions/predictions_yolo.json \
    --arrows data/arrows_output/arrows_detected.json \
    --output outputs/visualizacoes
```

As imagens geradas mostram:
- **Boxes verdes**: Componentes detectados (API, Database, etc.)
- **Boxes azuis**: Setas/conexões detectadas
- **Círculos amarelos**: Início da seta
- **Círculos vermelhos**: Ponta da seta
- **Labels**: Nome do componente + confiança

### Etapas Individuais

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

### Visualizações

As imagens processadas ficam em `outputs/visualizacoes/`:

```
outputs/visualizacoes/
├── imagem_1_detected.png    # Imagem com boxes e arrows desenhadas
├── imagem_2_detected.png
└── imagem_3_detected.png
```

**Legenda das visualizações:**
- 🟢 **Box verde**: Componente detectado (ex: "aws_api_gateway: 0.87")
- 🔵 **Box azul**: Seta/conexão detectada
- 🟡 **Círculo amarelo**: Início da seta (origem)
- 🔴 **Círculo vermelho**: Ponta da seta (destino)

### Resultados STRIDE

Cada execução cria uma pasta versionada com timestamp:

```
outputs/
├── run_2026_03_06_112153/           # Pasta versionada por execução
│   ├── predictions_yolo.json        # Componentes detectados
│   ├── arrows_detected.json         # Setas detectadas
│   ├── connections.json             # Conexões mapeadas (origem → destino)
│   ├── threat_model_completo.json   # Ameaças base + contextuais (JSON)
│   ├── stride_completo.md           # Relatório STRIDE integrado (Markdown)
│   └── visualizacoes/               # ✨ Imagens com detecções desenhadas
│       ├── imagem_1_detected.png
│       ├── imagem_2_detected.png
│       └── imagem_3_detected.png
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
- Visualizações organizadas por run




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

## Troubleshooting

### Imagens sem detecções desenhadas?

Se os modelos não estão gerando as imagens com boxes e arrows:

1. **Instale as dependências de visualização:**
```bash
pip install opencv-python numpy
```

2. **Execute o pipeline completo:**
```bash
python scripts/pipeline_completo.py --input imagens_validacao
```

3. **Ou gere apenas as visualizações:**
```bash
python scripts/visualizar_deteccoes.py
```

### Modelos não encontrados?

Certifique-se que os arquivos estão em:
- `models/best_icons.pt` (18MB)
- `models/best_arrows.pt` (19MB)

### Erro de device (MPS/CUDA)?

Use `--device cpu` se não tiver GPU:
```bash
python scripts/pipeline_completo.py --device cpu
```

## Licença

Projeto desenvolvido para o Hackathon FIAP Software Security.
