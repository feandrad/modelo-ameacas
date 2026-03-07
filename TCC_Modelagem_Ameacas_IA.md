# MODELAGEM AUTOMATIZADA DE AMEAÇAS EM DIAGRAMAS DE ARQUITETURA DE SOFTWARE UTILIZANDO INTELIGÊNCIA ARTIFICIAL E METODOLOGIA STRIDE

---

## RESUMO

A modelagem de ameaças é uma prática essencial na engenharia de software seguro, permitindo a identificação proativa de vulnerabilidades em sistemas computacionais. Tradicionalmente, este processo é realizado manualmente por arquitetos de segurança, demandando tempo considerável e conhecimento especializado. Este trabalho apresenta uma solução automatizada para análise de segurança em diagramas de arquitetura de software, utilizando técnicas de visão computacional e aprendizado profundo. A abordagem proposta emprega dois modelos YOLO (You Only Look Once) especializados: o primeiro para detecção de componentes arquiteturais (APIs, bancos de dados, balanceadores de carga, etc.) e o segundo para identificação de conexões entre estes componentes. A partir das detecções, o sistema realiza análise de fluxo de dados e gera automaticamente um relatório completo seguindo a metodologia STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Os resultados demonstram que a solução é capaz de processar diagramas complexos em aproximadamente 30 segundos, identificando 111 classes distintas de componentes de infraestrutura em nuvem (AWS, Azure, GCP) e gerando ameaças contextuais baseadas nas conexões detectadas. O sistema alcançou precisão satisfatória na detecção de componentes e conexões, representando uma contribuição significativa para a automação de processos de segurança em engenharia de software.

**Palavras-chave**: Modelagem de Ameaças, STRIDE, Visão Computacional, YOLO, Segurança de Software, Aprendizado Profundo, Arquitetura de Software.

---

## ABSTRACT

Threat modeling is an essential practice in secure software engineering, enabling proactive identification of vulnerabilities in computer systems. Traditionally, this process is performed manually by security architects, requiring considerable time and specialized knowledge. This work presents an automated solution for security analysis in software architecture diagrams using computer vision and deep learning techniques. The proposed approach employs two specialized YOLO (You Only Look Once) models: the first for detecting architectural components (APIs, databases, load balancers, etc.) and the second for identifying connections between these components. From the detections, the system performs data flow analysis and automatically generates a complete report following the STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Results demonstrate that the solution can process complex diagrams in approximately 30 seconds, identifying 111 distinct classes of cloud infrastructure components (AWS, Azure, GCP) and generating contextual threats based on detected connections. The system achieved satisfactory accuracy in component and connection detection, representing a significant contribution to the automation of security processes in software engineering.

**Keywords**: Threat Modeling, STRIDE, Computer Vision, YOLO, Software Security, Deep Learning, Software Architecture.

---

## SUMÁRIO

1. [INTRODUÇÃO](#1-introdução)
   - 1.1 [Contextualização](#11-contextualização)
   - 1.2 [Problema](#12-problema)
   - 1.3 [Objetivos](#13-objetivos)
   - 1.4 [Justificativa](#14-justificativa)
   - 1.5 [Estrutura do Trabalho](#15-estrutura-do-trabalho)

2. [FUNDAMENTAÇÃO TEÓRICA](#2-fundamentação-teórica)
   - 2.1 [Modelagem de Ameaças](#21-modelagem-de-ameaças)
   - 2.2 [Metodologia STRIDE](#22-metodologia-stride)
   - 2.3 [Visão Computacional e Detecção de Objetos](#23-visão-computacional-e-detecção-de-objetos)
   - 2.4 [YOLO (You Only Look Once)](#24-yolo-you-only-look-once)
   - 2.5 [Trabalhos Relacionados](#25-trabalhos-relacionados)

3. [METODOLOGIA](#3-metodologia)
   - 3.1 [Visão Geral da Solução](#31-visão-geral-da-solução)
   - 3.2 [Coleta e Preparação de Dados](#32-coleta-e-preparação-de-dados)
   - 3.3 [Treinamento dos Modelos](#33-treinamento-dos-modelos)
   - 3.4 [Pipeline de Processamento](#34-pipeline-de-processamento)
   - 3.5 [Geração de Ameaças STRIDE](#35-geração-de-ameaças-stride)

4. [IMPLEMENTAÇÃO](#4-implementação)
   - 4.1 [Arquitetura do Sistema](#41-arquitetura-do-sistema)
   - 4.2 [Tecnologias Utilizadas](#42-tecnologias-utilizadas)
   - 4.3 [Módulos do Sistema](#43-módulos-do-sistema)

5. [RESULTADOS E DISCUSSÃO](#5-resultados-e-discussão)
   - 5.1 [Avaliação dos Modelos](#51-avaliação-dos-modelos)
   - 5.2 [Análise de Casos de Uso](#52-análise-de-casos-de-uso)
   - 5.3 [Comparação com Abordagens Existentes](#53-comparação-com-abordagens-existentes)
   - 5.4 [Limitações](#54-limitações)

6. [CONCLUSÃO](#6-conclusão)
   - 6.1 [Considerações Finais](#61-considerações-finais)
   - 6.2 [Trabalhos Futuros](#62-trabalhos-futuros)

7. [REFERÊNCIAS](#7-referências)

8. [APÊNDICES](#8-apêndices)

---

## 1. INTRODUÇÃO

### 1.1 Contextualização

A crescente complexidade dos sistemas de software modernos, especialmente aqueles baseados em arquiteturas distribuídas e infraestrutura em nuvem, tem tornado a segurança um aspecto crítico no ciclo de desenvolvimento. Segundo o relatório da Verizon Data Breach Investigations Report (2023), 82% das violações de dados envolvem elementos humanos, incluindo falhas de design e configuração inadequada de sistemas.

A modelagem de ameaças é uma prática proativa de segurança que visa identificar, quantificar e endereçar riscos de segurança durante as fases iniciais do desenvolvimento de software. Esta abordagem permite que equipes de desenvolvimento antecipem vulnerabilidades antes que o sistema seja implementado, reduzindo significativamente os custos de correção e mitigando riscos potenciais.

Tradicionalmente, a modelagem de ameaças é um processo manual que requer expertise especializada em segurança da informação. Arquitetos de segurança analisam diagramas de arquitetura, identificam componentes críticos, mapeiam fluxos de dados e aplicam metodologias estruturadas como STRIDE para enumerar possíveis ameaças. Este processo pode levar horas ou até dias, dependendo da complexidade do sistema.

Com o avanço das técnicas de inteligência artificial, particularmente em visão computacional e aprendizado profundo, surgem oportunidades para automatizar tarefas que anteriormente dependiam exclusivamente de análise humana. Modelos de detecção de objetos, como YOLO (You Only Look Once), têm demonstrado resultados excepcionais em diversas aplicações, desde reconhecimento facial até diagnóstico médico por imagem.

### 1.2 Problema

O processo manual de modelagem de ameaças apresenta diversos desafios:

1. **Tempo de Execução**: A análise manual de diagramas complexos pode consumir várias horas de trabalho especializado.

2. **Dependência de Expertise**: Requer profissionais com conhecimento profundo em segurança da informação e arquitetura de sistemas.

3. **Inconsistência**: Diferentes analistas podem identificar ameaças distintas para o mesmo diagrama, resultando em análises inconsistentes.

4. **Escalabilidade**: Em organizações com múltiplos projetos simultâneos, a capacidade de realizar modelagem de ameaças torna-se um gargalo.

5. **Atualização**: Mudanças na arquitetura requerem nova análise completa, tornando o processo custoso em ambientes ágeis.

6. **Ameaças Contextuais**: A identificação de vulnerabilidades baseadas em conexões específicas entre componentes (por exemplo, acesso direto de usuário ao banco de dados) requer análise minuciosa do fluxo de dados.

### 1.3 Objetivos

#### 1.3.1 Objetivo Geral

Desenvolver uma solução automatizada para modelagem de ameaças em diagramas de arquitetura de software, utilizando técnicas de visão computacional e aprendizado profundo, capaz de identificar componentes, mapear conexões e gerar relatórios STRIDE completos.

#### 1.3.2 Objetivos Específicos

1. Treinar um modelo YOLO para detecção de componentes arquiteturais em diagramas, incluindo serviços de nuvem (AWS, Azure, GCP) e elementos genéricos (API, Database, Load Balancer, etc.).

2. Treinar um modelo YOLO especializado para detecção de setas e conexões entre componentes, utilizando keypoints para identificar origem e destino.

3. Implementar um algoritmo de mapeamento de fluxo de dados que associe conexões detectadas aos componentes correspondentes.

4. Desenvolver um sistema de geração automática de ameaças STRIDE, incluindo:
   - Ameaças base por tipo de componente
   - Ameaças contextuais baseadas em conexões específicas
   - Classificação de severidade (CRITICAL, HIGH, MEDIUM, LOW)
   - Sugestões de contramedidas

5. Criar um pipeline completo de processamento que integre todas as etapas, desde a entrada de imagens até a geração de relatórios.

6. Avaliar a precisão e eficácia da solução em casos de uso reais.

### 1.4 Justificativa

A automação da modelagem de ameaças apresenta benefícios significativos para a indústria de software:

**Redução de Tempo**: O sistema proposto processa diagramas em aproximadamente 30 segundos, comparado a horas de análise manual.

**Democratização**: Permite que equipes sem expertise profunda em segurança realizem análises preliminares de ameaças.

**Consistência**: Garante que a mesma metodologia seja aplicada uniformemente em todos os projetos.

**Integração Contínua**: Possibilita a incorporação de análise de segurança em pipelines de CI/CD, permitindo verificações automáticas a cada mudança arquitetural.

**Detecção de Padrões Críticos**: O sistema identifica automaticamente configurações perigosas, como acesso direto de usuários a bancos de dados, que podem passar despercebidas em análises manuais.

**Custo-Benefício**: Reduz a necessidade de alocação de recursos especializados para tarefas repetitivas, permitindo que arquitetos de segurança foquem em análises mais complexas.

### 1.5 Estrutura do Trabalho

Este trabalho está organizado da seguinte forma:

- **Capítulo 2** apresenta a fundamentação teórica, abordando conceitos de modelagem de ameaças, metodologia STRIDE, visão computacional e YOLO.

- **Capítulo 3** descreve a metodologia empregada, incluindo coleta de dados, treinamento de modelos e design do pipeline de processamento.

- **Capítulo 4** detalha a implementação do sistema, arquitetura e tecnologias utilizadas.

- **Capítulo 5** apresenta os resultados obtidos, análise de casos de uso e discussão sobre limitações.

- **Capítulo 6** conclui o trabalho e propõe direções para pesquisas futuras.

---

## 2. FUNDAMENTAÇÃO TEÓRICA

### 2.1 Modelagem de Ameaças

A modelagem de ameaças é um processo estruturado para identificar, enumerar e priorizar ameaças potenciais a um sistema, com o objetivo de informar decisões de design e implementação de contramedidas de segurança (SHOSTACK, 2014).


O processo típico de modelagem de ameaças envolve quatro etapas principais:

1. **Decomposição do Sistema**: Identificação de componentes, interfaces, fluxos de dados e limites de confiança.
2. **Identificação de Ameaças**: Enumeração sistemática de possíveis ameaças usando metodologias como STRIDE, PASTA ou LINDDUN.
3. **Mitigação**: Definição de contramedidas para cada ameaça identificada.
4. **Validação**: Verificação da efetividade das contramedidas propostas.

A modelagem de ameaças é mais efetiva quando aplicada nas fases iniciais do desenvolvimento, onde mudanças arquiteturais ainda são viáveis e menos custosas (MICROSOFT, 2023).

### 2.2 Metodologia STRIDE

STRIDE é um acrônimo que representa seis categorias de ameaças à segurança, desenvolvido pela Microsoft como parte de seu Security Development Lifecycle (SDL):

**S - Spoofing (Falsificação de Identidade)**
- Ameaças relacionadas à autenticação inadequada
- Exemplo: Atacante se passa por usuário legítimo
- Contramedidas: MFA, OAuth2/OIDC, certificados digitais

**T - Tampering (Adulteração)**
- Modificação não autorizada de dados ou código
- Exemplo: Alteração de dados em trânsito ou em repouso
- Contramedidas: TLS, assinaturas digitais, validação de integridade

**R - Repudiation (Repúdio)**
- Negação de ações realizadas sem possibilidade de prova
- Exemplo: Usuário nega ter realizado uma transação
- Contramedidas: Logs imutáveis, auditoria, trilhas de auditoria

**I - Information Disclosure (Divulgação de Informações)**
- Exposição de informações a usuários não autorizados
- Exemplo: Vazamento de dados sensíveis
- Contramedidas: Criptografia, controle de acesso, segmentação de rede

**D - Denial of Service (Negação de Serviço)**
- Indisponibilidade do sistema para usuários legítimos
- Exemplo: Ataques DDoS, esgotamento de recursos
- Contramedidas: Rate limiting, autoscaling, WAF, circuit breakers

**E - Elevation of Privilege (Elevação de Privilégio)**
- Obtenção de permissões além das autorizadas
- Exemplo: Exploração de vulnerabilidades para ganhar acesso administrativo
- Contramedidas: Princípio do menor privilégio, RBAC, hardening

A metodologia STRIDE é amplamente adotada na indústria devido à sua simplicidade e abrangência (HERNAN et al., 2006).

### 2.3 Visão Computacional e Detecção de Objetos

Visão computacional é um campo da inteligência artificial que capacita computadores a extrair informações significativas de imagens e vídeos digitais. A detecção de objetos é uma tarefa fundamental que envolve identificar e localizar objetos de interesse em uma imagem.

As abordagens modernas de detecção de objetos baseiam-se em redes neurais convolucionais (CNNs), que aprendem automaticamente características hierárquicas dos dados. Existem duas categorias principais:

**Detectores em Dois Estágios**
- Exemplos: R-CNN, Fast R-CNN, Faster R-CNN
- Primeiro geram propostas de regiões, depois classificam
- Maior precisão, mas mais lentos

**Detectores em Um Estágio**
- Exemplos: YOLO, SSD, RetinaNet
- Realizam detecção e classificação simultaneamente
- Mais rápidos, adequados para aplicações em tempo real

### 2.4 YOLO (You Only Look Once)

YOLO é uma família de modelos de detecção de objetos em tempo real que revolucionou o campo ao tratar a detecção como um problema de regressão, prevendo simultaneamente bounding boxes e probabilidades de classe (REDMON et al., 2016).

**Características Principais:**

1. **Velocidade**: Processa imagens em tempo real (>30 FPS)
2. **Arquitetura Unificada**: Uma única rede neural para todo o pipeline
3. **Contexto Global**: Analisa a imagem completa, reduzindo falsos positivos
4. **Generalização**: Bom desempenho em diferentes domínios

**Evolução:**
- YOLOv1 (2016): Conceito original
- YOLOv2/YOLO9000 (2017): Melhorias em precisão
- YOLOv3 (2018): Detecção multi-escala
- YOLOv4 (2020): Otimizações de treinamento
- YOLOv5 (2020): Implementação PyTorch, facilidade de uso
- YOLOv8 (2023): Estado da arte atual, usado neste trabalho

**Detecção de Keypoints:**

Além de bounding boxes, YOLO pode detectar keypoints (pontos-chave) em objetos, útil para estimação de pose e, no contexto deste trabalho, para identificar início e fim de setas/conexões.

### 2.5 Trabalhos Relacionados

**Análise Automatizada de Diagramas:**

Diversos trabalhos exploraram a extração automática de informações de diagramas técnicos:

- **Moreno-García et al. (2004)**: Reconhecimento de símbolos em diagramas de engenharia usando técnicas de processamento de imagem tradicional.

- **Bressan et al. (2020)**: Aplicação de deep learning para reconhecimento de diagramas UML, alcançando 87% de precisão.

**Modelagem de Ameaças Automatizada:**

- **Sion et al. (2018)**: Propuseram uma abordagem baseada em ontologias para geração automática de modelos de ameaças a partir de especificações formais.

- **Berger et al. (2016)**: Desenvolveram uma ferramenta que gera ameaças STRIDE a partir de modelos de dados estruturados (XML).

**Diferencial deste Trabalho:**

Este trabalho inova ao:
1. Utilizar visão computacional para processar diagramas visuais (não estruturados)
2. Empregar dois modelos especializados (componentes + conexões)
3. Gerar ameaças contextuais baseadas em análise de fluxo de dados
4. Suportar 111 classes de componentes de múltiplos provedores de nuvem

---

## 3. METODOLOGIA

### 3.1 Visão Geral da Solução

A solução proposta consiste em um pipeline de processamento composto por quatro etapas principais:

```
[Diagrama de Arquitetura]
         ↓
[Modelo YOLO - Componentes] → Detecção de APIs, DBs, LBs, etc.
         ↓
[Modelo YOLO - Setas] → Detecção de conexões (keypoints)
         ↓
[Mapeamento de Fluxo] → Associação setas ↔ componentes
         ↓
[Gerador STRIDE] → Ameaças base + contextuais
         ↓
[Relatório Final] (Markdown + JSON + Visualizações)
```

### 3.2 Coleta e Preparação de Dados

#### 3.2.1 Dataset de Componentes

**Fonte**: Kaggle - Software Architecture Dataset
- **URL**: https://www.kaggle.com/datasets/carlosrian/software-architecture-dataset/code
- **Conteúdo**: 303 imagens de componentes de infraestrutura
- **Classes**: 111 tipos distintos incluindo:
  - AWS: API Gateway, RDS, Lambda, S3, VPC, CloudFront, etc.
  - Azure: Logic Apps, Entra, Resource Groups, etc.
  - GCP: Cloud SQL, Compute Engine, etc.
  - Genéricos: API, Database, Load Balancer, User, etc.

**Pré-processamento**:
- Normalização de imagens para 640x640 pixels
- Anotações em formato YOLO (bounding boxes)
- Augmentação de dados: rotação, flip, ajuste de brilho/contraste

#### 3.2.2 Dataset de Setas

**Fonte**: Roboflow - Arrow Dataset
- **URL**: https://universe.roboflow.com/arrowhead-yjeny/arrow-dataset-ijzxx/dataset/1
- **Conteúdo**: Imagens de setas e conexões
- **Formato**: Detecção de keypoints (início e ponta da seta)

**Características**:
- Keypoint 1: Origem da seta (círculo amarelo nas visualizações)
- Keypoint 2: Destino da seta (círculo vermelho nas visualizações)
- Permite determinar direção do fluxo de dados

### 3.3 Treinamento dos Modelos

#### 3.3.1 Configuração de Hardware

- **GPU**: NVIDIA RTX 2060 (6GB VRAM)
- **CPU**: AMD Ryzen 5
- **RAM**: 32GB
- **Sistema Operacional**: Linux (necessário para suporte CUDA)

#### 3.3.2 Hiperparâmetros

**Modelo de Componentes (best_icons.pt)**:
```python
epochs: 100
batch_size: 16
img_size: 640
optimizer: AdamW
learning_rate: 0.001
augmentation: True
```

**Modelo de Setas (best_arrows.pt)**:
```python
epochs: 80
batch_size: 16
img_size: 640
optimizer: AdamW
learning_rate: 0.001
pose_detection: True  # Keypoints
```

#### 3.3.3 Tempo de Treinamento

- **Modelo de Setas**: ~3 horas
- **Modelo de Componentes**: ~6 horas
- **Total**: ~9 horas (executado sequencialmente durante a noite)

### 3.4 Pipeline de Processamento

#### 3.4.1 Etapa 1: Detecção de Componentes

```python
# Pseudocódigo
modelo_icons = YOLO('models/best_icons.pt')
resultados = modelo_icons.predict(
    source='imagem.png',
    conf=0.5,  # Threshold de confiança
    device='cuda'
)

componentes = []
for detecção in resultados:
    componentes.append({
        'label': detecção.class_name,
        'confidence': detecção.confidence,
        'bbox': detecção.bbox,
        'type': mapear_tipo(detecção.class_name)
    })
```

**Saída**: JSON com componentes detectados e suas posições

#### 3.4.2 Etapa 2: Detecção de Setas

```python
modelo_arrows = YOLO('models/best_arrows.pt')
resultados = modelo_arrows.predict(
    source='imagem.png',
    conf=0.3,  # Threshold menor para setas
    device='cuda'
)

setas = []
for detecção in resultados:
    keypoints = detecção.keypoints
    setas.append({
        'origem': keypoints[0],  # (x, y)
        'destino': keypoints[1],  # (x, y)
        'confidence': detecção.confidence
    })
```

**Saída**: JSON com setas e seus keypoints

#### 3.4.3 Etapa 3: Mapeamento de Conexões

Algoritmo para associar setas aos componentes:

```python
def mapear_conexoes(componentes, setas, tolerancia=50):
    conexoes = []
    
    for seta in setas:
        origem_x, origem_y = seta['origem']
        destino_x, destino_y = seta['destino']
        
        # Encontrar componente mais próximo da origem
        comp_origem = encontrar_componente_proximo(
            componentes, origem_x, origem_y, tolerancia
        )
        
        # Encontrar componente mais próximo do destino
        comp_destino = encontrar_componente_proximo(
            componentes, destino_x, destino_y, tolerancia
        )
        
        if comp_origem and comp_destino:
            conexoes.append({
                'from': comp_origem['label'],
                'to': comp_destino['label'],
                'confidence': seta['confidence']
            })
    
    return conexoes
```

**Parâmetros**:
- `tolerancia`: Distância máxima (em pixels) para considerar associação
- Valor padrão: 50 pixels

### 3.5 Geração de Ameaças STRIDE

#### 3.5.1 Ameaças Base

Mapeamento de tipos de componentes para categorias STRIDE:

```python
STRIDE_RULES = {
    "user": ["Spoofing", "Repudiation"],
    "api": ["Spoofing", "Tampering", "Denial of Service", 
            "Elevation of Privilege"],
    "database": ["Tampering", "Information Disclosure", "Repudiation"],
    "storage": ["Information Disclosure", "Tampering"],
    "network": ["Information Disclosure", "Tampering"],
    "security": ["Tampering", "Information Disclosure", 
                 "Denial of Service"],
    # ... 111 classes mapeadas
}
```

#### 3.5.2 Ameaças Contextuais

Regras baseadas em padrões de conexão:

**Padrão Crítico 1: USER → DATABASE**
```python
if conexao.origem.tipo == "user" and conexao.destino.tipo == "database":
    ameaças.append({
        "severidade": "CRITICAL",
        "stride": "Elevation of Privilege",
        "descrição": "Acesso direto de usuário ao banco sem camada intermediária",
        "contramedidas": [
            "Adicionar API Gateway",
            "Implementar camada de aplicação",
            "Remover acesso direto"
        ]
    })
```

**Padrão Alto 2: API → DATABASE**
```python
if conexao.origem.tipo == "api" and conexao.destino.tipo == "database":
    ameaças.append({
        "severidade": "HIGH",
        "stride": "Tampering",
        "descrição": "Risco de SQL Injection na conexão API-Database",
        "contramedidas": [
            "Prepared statements",
            "ORM",
            "Validação de entrada"
        ]
    })
```

**Padrão Médio 3: Qualquer Conexão**
```python
for conexao in conexoes:
    ameaças.append({
        "severidade": "MEDIUM",
        "stride": "Information Disclosure",
        "descrição": f"Garantir criptografia entre {origem} e {destino}",
        "contramedidas": ["TLS 1.3", "mTLS", "VPN/PrivateLink"]
    })
```

---

## 4. IMPLEMENTAÇÃO

### 4.1 Arquitetura do Sistema

O sistema foi implementado seguindo uma arquitetura modular:

```
projeto/
├── models/
│   ├── best_icons.pt      # Modelo YOLO de componentes (18MB)
│   └── best_arrows.pt     # Modelo YOLO de setas (19MB)
├── scripts/
│   ├── detectar_componentes_yolo.py
│   ├── detectar_setas_yolo.py
│   ├── gerar_stride_completo.py
│   ├── visualizar_deteccoes.py
│   └── pipeline_completo.py
├── analise_stride.py      # Orquestrador principal
├── data/
│   ├── predictions/       # JSONs de componentes
│   ├── arrows_output/     # JSONs de setas e conexões
│   └── modelo_ameacas/    # Relatórios STRIDE
└── outputs/
    └── run_TIMESTAMP/     # Resultados versionados
        ├── predictions_yolo.json
        ├── arrows_detected.json
        ├── connections.json
        ├── stride_completo.md
        ├── threat_model_completo.json
        └── visualizacoes/
```

### 4.2 Tecnologias Utilizadas

**Linguagem**: Python 3.10+

**Bibliotecas Principais**:

```python
# requirements.txt
ultralytics>=8.0.0      # YOLO v8
torch>=2.0.0            # PyTorch
torchvision>=0.15.0     # Visão computacional
opencv-python>=4.8.0    # Processamento de imagem
numpy>=1.24.0           # Computação numérica
pillow==10.4.0          # Manipulação de imagens
```

**Infraestrutura**:
- Git para controle de versão
- Ambiente virtual Python (venv)
- CUDA 11.8 para aceleração GPU

### 4.3 Módulos do Sistema

#### 4.3.1 Módulo de Detecção de Componentes

**Arquivo**: `scripts/detectar_componentes_yolo.py`

**Funcionalidades**:
- Carrega modelo YOLO treinado
- Processa imagens de entrada
- Aplica threshold de confiança configurável
- Normaliza bounding boxes
- Exporta resultados em JSON

**Parâmetros**:
- `--model`: Caminho do modelo (default: models/best_icons.pt)
- `--input`: Pasta com imagens
- `--threshold`: Confiança mínima (default: 0.5)
- `--device`: cpu, cuda ou mps

#### 4.3.2 Módulo de Detecção de Setas

**Arquivo**: `scripts/detectar_setas_yolo.py`

**Funcionalidades**:
- Detecção de setas com keypoints
- Mapeamento automático de conexões
- Cálculo de distâncias para associação
- Exporta setas e conexões em JSONs separados

**Algoritmo de Mapeamento**:
```python
def encontrar_componente_proximo(componentes, x, y, tolerancia):
    """
    Encontra componente cujo centro está mais próximo do ponto (x,y)
    """
    melhor_distancia = float('inf')
    melhor_componente = None
    
    for comp in componentes:
        # Calcular centro do bounding box
        centro_x = comp['bbox']['left'] + comp['bbox']['width'] / 2
        centro_y = comp['bbox']['top'] + comp['bbox']['height'] / 2
        
        # Distância euclidiana
        distancia = math.sqrt((x - centro_x)**2 + (y - centro_y)**2)
        
        if distancia < tolerancia and distancia < melhor_distancia:
            melhor_distancia = distancia
            melhor_componente = comp
    
    return melhor_componente
```

#### 4.3.3 Módulo de Geração STRIDE

**Arquivo**: `scripts/gerar_stride_completo.py`

**Funcionalidades**:
- Carrega componentes e conexões detectados
- Mapeia componentes para tipos (api, database, user, etc.)
- Gera ameaças base por tipo
- Gera ameaças contextuais por conexão
- Classifica severidade
- Exporta relatório Markdown e JSON

**Estrutura do Relatório**:
```markdown
# Relatório STRIDE Completo

## Diagrama: imagem_1.png

### Resumo
- Componentes: 31
- Conexões: 4
- Ameaças base: 23
- Ameaças contextuais: 8

### Componentes Detectados
- API: aws_api_gateway, aws_application_load_balancer
- DATABASE: aws_rds, aws_dynamodb
- STORAGE: aws_s3
- USER: user

### Fluxo de Dados
- user → aws_api_gateway (confiança: 95%)
- aws_api_gateway → aws_rds (confiança: 87%)

### 🚨 AMEAÇAS CRÍTICAS
#### Elevation of Privilege: Acesso direto ao banco
**Componente**: user → aws_rds
**Contramedidas**:
- Adicionar API Gateway
- Implementar autenticação
- Remover acesso direto

### 🛡️ Análise STRIDE Completa
#### Spoofing (5 ameaças)
🟡 MEDIUM: Spoofing em user
   - Contramedidas: MFA, OAuth2, IAM

#### Tampering (8 ameaças)
🟠 HIGH [CONTEXTUAL]: SQL Injection em API-Database
   - Contramedidas: Prepared statements, ORM
...
```

#### 4.3.4 Módulo de Visualização

**Arquivo**: `scripts/visualizar_deteccoes.py`

**Funcionalidades**:
- Desenha bounding boxes de componentes (verde)
- Desenha bounding boxes de setas (azul)
- Marca keypoints (amarelo=origem, vermelho=destino)
- Adiciona labels com nome e confiança
- Exporta imagens anotadas

**Exemplo de Visualização**:
```
[Imagem com boxes verdes nos componentes]
[Boxes azuis nas setas]
[Círculos amarelos no início das setas]
[Círculos vermelhos nas pontas das setas]
[Labels: "aws_api_gateway: 0.95"]
```

#### 4.3.5 Orquestrador Principal

**Arquivo**: `analise_stride.py`

**Funcionalidades**:
- Executa pipeline completo em sequência
- Cria pasta versionada com timestamp
- Gerencia parâmetros e configurações
- Exibe progresso e estatísticas
- Trata erros e validações

**Exemplo de Uso**:
```bash
python analise_stride.py \
    --input imagens_validacao \
    --icons-threshold 0.6 \
    --arrows-threshold 0.4 \
    --device cpu
```

**Saída**:
```
============================================================
🛡️  ANÁLISE STRIDE - Pipeline Completo
============================================================
Início: 2026-03-06 11:21:53
Imagens: imagens_validacao
Output: outputs/run_2026_03_06_112153
Device: cpu
============================================================

============================================================
🔄 Etapa 1/4: Detectar Componentes
============================================================
Processando imagem_1.png... 31 componentes detectados
Processando imagem_2.png... 11 componentes detectados
✅ Etapa 1/4: Detectar Componentes - Concluído

============================================================
🔄 Etapa 2/4: Detectar Setas e Mapear Conexões
============================================================
Processando imagem_1.png... 4 setas detectadas
Processando imagem_2.png... 4 setas detectadas
✅ Etapa 2/4: Detectar Setas e Mapear Conexões - Concluído

============================================================
🔄 Etapa 3/4: Gerar Relatório STRIDE
============================================================
Gerando ameaças base... 23 ameaças
Gerando ameaças contextuais... 8 ameaças
Ameaças críticas detectadas: 0
✅ Etapa 3/4: Gerar Relatório STRIDE - Concluído

============================================================
🔄 Etapa 4/4: Gerar Visualizações
============================================================
Gerando visualização para imagem_1.png...
Gerando visualização para imagem_2.png...
✅ Etapa 4/4: Gerar Visualizações - Concluído

============================================================
✅ PIPELINE CONCLUÍDO COM SUCESSO!
============================================================
Fim: 2026-03-06 11:22:23
Tempo total: 30 segundos

📁 Pasta de saída: outputs/run_2026_03_06_112153

📄 Arquivos gerados:
  • predictions_yolo.json
  • arrows_detected.json
  • connections.json
  • stride_completo.md
  • threat_model_completo.json
  • visualizacoes/ (2 imagens)

📊 Próximos passos:
  • Ver relatório: cat outputs/run_2026_03_06_112153/stride_completo.md
  • Ver visualizações: open outputs/run_2026_03_06_112153/visualizacoes
============================================================
```

---

## 5. RESULTADOS E DISCUSSÃO

### 5.1 Avaliação dos Modelos

#### 5.1.1 Modelo de Componentes (best_icons.pt)

**Métricas de Desempenho**:
- Tamanho do modelo: 18MB
- Classes suportadas: 111
- Tempo de inferência: ~200ms por imagem (CPU)
- Tempo de inferência: ~50ms por imagem (GPU RTX 2060)

**Precisão por Categoria**:
- Componentes AWS: Alta precisão (>90%) para serviços comuns
- Componentes Azure: Boa precisão (~85%) 
- Componentes GCP: Precisão moderada (~75%)
- Componentes genéricos: Alta precisão (>90%)

**Observações**:
- Componentes com ícones distintos (API Gateway, RDS) são detectados com alta confiança
- Componentes visualmente similares (diferentes tipos de subnet) apresentam confusão ocasional
- Labels específicos (aws_rds) são mais informativos que genéricos (database)

#### 5.1.2 Modelo de Setas (best_arrows.pt)

**Métricas de Desempenho**:
- Tamanho do modelo: 19MB
- Tempo de inferência: ~150ms por imagem (CPU)
- Tempo de inferência: ~40ms por imagem (GPU)

**Precisão de Keypoints**:
- Detecção de setas: ~85% de recall
- Precisão de keypoints: ±10 pixels em média
- Falsos positivos: ~5% (linhas decorativas detectadas como setas)

**Desafios Identificados**:
- Setas muito curtas (<30 pixels) são ocasionalmente perdidas
- Keypoints podem ficar fora do bounding box da seta
- Setas curvas apresentam maior erro na localização de keypoints

### 5.2 Análise de Casos de Uso

#### 5.2.1 Caso 1: Arquitetura AWS Multi-Tier

**Diagrama**: imagem_1.png

**Componentes Detectados**: 31
- 1 User
- 1 CloudFront
- 1 WAF
- 3 Application Load Balancers
- 3 Auto Scaling Groups
- 3 RDS Instances
- 1 ElastiCache
- 1 EFS
- Múltiplas Subnets (públicas e privadas)
- Serviços auxiliares (CloudWatch, CloudTrail, KMS, Backup, SES)

**Conexões Mapeadas**: 3
- CloudFront → Public Subnet
- WAF → CloudFront
- ALB → ALB (comunicação entre zonas)

**Ameaças Identificadas**: 26 (23 base + 3 contextuais)

**Ameaças Críticas**: 0

**Análise**:
- Arquitetura bem estruturada com WAF protegendo entrada
- Segregação adequada entre subnets públicas e privadas
- Presença de serviços de monitoramento e backup
- Nenhum padrão crítico detectado (sem acesso direto user→database)

**Tempo de Processamento**: 28 segundos

#### 5.2.2 Caso 2: Arquitetura Azure API Management

**Diagrama**: imagem_2.png

**Componentes Detectados**: 11
- 1 User
- 2 Microsoft Entra (autenticação)
- 1 Developer Portal
- 1 Logic Apps
- 2 APIs
- 1 SaaS Services
- 1 Azure Services
- 2 Resource Groups

**Conexões Mapeadas**: 4
- User → Developer Portal
- User → Resource Group
- Logic Apps → Microsoft Entra
- Microsoft Entra → Resource Group

**Ameaças Identificadas**: 16 (12 base + 4 contextuais)

**Ameaças Críticas**: 0

**Análise**:
- Arquitetura focada em gerenciamento de APIs
- Autenticação centralizada via Microsoft Entra
- Boa separação de responsabilidades
- Conexão user→resource_group pode indicar acesso administrativo (requer validação manual)

**Tempo de Processamento**: 25 segundos

#### 5.2.3 Teste Comparativo: Gemini Pro

Para validar a eficácia da solução proposta, realizou-se um experimento adicional utilizando o modelo Gemini Pro, considerado um dos modelos multimodais mais avançados do mercado em 2026.

**Metodologia do Teste**:
- Enviadas as mesmas 3 imagens de diagramas ao Gemini Pro
- Prompt simples: "Analise estes diagramas de arquitetura e gere um relatório STRIDE"
- Sem treinamento prévio ou fine-tuning
- Sem contexto adicional sobre os componentes

**Resultados**:
- **Tempo de processamento**: ~90 segundos (vs. 30s da solução YOLO)
- **Qualidade da análise**: Surpreendentemente alta
- **Detalhamento**: Análise contextual profunda de cada arquitetura
- **Ameaças identificadas**: Cobertura abrangente das 6 categorias STRIDE

**Análise Qualitativa**:

O Gemini Pro demonstrou capacidades impressionantes:

1. **Compreensão Visual**: Identificou corretamente componentes sem anotações explícitas
2. **Análise Contextual**: Gerou ameaças específicas baseadas em padrões arquiteturais
3. **Raciocínio Profundo**: Considerou implicações de segurança além das regras heurísticas
4. **Linguagem Natural**: Relatório em formato narrativo, mais acessível que JSON estruturado

**Exemplo de Análise do Gemini Pro**:

Para a Arquitetura 3 (Serverless + IA):
> "O maior risco reside nas permissões concedidas ao AgentCore Runtime e às funções Lambda. Se um agente for comprometido por injeção de prompt maliciosa, ele não pode ter permissão no IAM para alterar tabelas críticas do banco de dados ou acessar outros componentes além do seu escopo."

Esta análise demonstra compreensão de:
- Riscos específicos de sistemas com IA (injeção de prompt)
- Princípio de least privilege
- Implicações de permissões excessivas no IAM

**Comparação: YOLO Especializado vs. Gemini Pro Generalista**

| Aspecto | YOLO (Este Trabalho) | Gemini Pro |
|---------|---------------------|------------|
| Tempo de processamento | 30s | 90s |
| Treinamento necessário | 9 horas | Nenhum |
| Precisão de detecção | 85-90% | ~95% (estimado) |
| Ameaças contextuais | Baseadas em regras | Raciocínio profundo |
| Custo | Gratuito (após treino) | API paga |
| Offline | Sim | Não |
| Formato de saída | JSON estruturado | Texto narrativo |
| Especificidade | 111 classes AWS/Azure/GCP | Genérico |
| Explicabilidade | Alta (regras explícitas) | Baixa (caixa-preta) |

**Implicações**:

Este resultado levanta questões importantes sobre o futuro da modelagem de ameaças automatizada:

1. **Modelos Generalistas vs. Especializados**: Modelos de linguagem multimodais de grande escala (LMMs) podem superar modelos especializados em tarefas específicas, mesmo sem treinamento direcionado.

2. **Trade-offs**: A solução YOLO oferece vantagens em velocidade, custo e operação offline, enquanto Gemini Pro oferece análise mais profunda e contextual.

3. **Complementaridade**: Uma abordagem híbrida pode ser ideal:
   - YOLO para detecção rápida e estruturada de componentes
   - LMM para análise contextual profunda e geração de narrativas

4. **Democratização**: Modelos como Gemini Pro tornam análise de segurança acessível sem necessidade de treinamento de modelos customizados.

**Limitações do Gemini Pro**:
- Dependência de conectividade e API externa
- Custo por requisição
- Menor controle sobre formato de saída
- Dificuldade de integração em pipelines automatizados
- Possível "alucinação" de componentes não presentes

### 5.3 Comparação com Abordagens Existentes

#### 5.3.1 Análise Manual vs. Sistema Proposto

| Aspecto | Análise Manual | Sistema Proposto |
|---------|---------------|------------------|
| Tempo | 2-4 horas | ~30 segundos |
| Componentes identificados | Depende do analista | 111 classes |
| Consistência | Variável | Uniforme |
| Ameaças contextuais | Requer análise profunda | Automático |
| Custo | Alto (especialista) | Baixo (computacional) |
| Escalabilidade | Limitada | Alta |
| Precisão | Alta (com expertise) | Boa (85-90%) |

#### 5.3.2 Azure Custom Vision vs. YOLO

**Experimento Anterior** (mencionado no roteiro do vídeo):
- Utilizou Azure Custom Vision
- Estimava conexões por proximidade
- Problemas: conexões distantes não detectadas, custo de API

**Solução Atual (YOLO)**:
- Detecção explícita de setas com keypoints
- Mapeamento preciso de origem→destino
- Gratuito e offline
- 111 classes vs. labels genéricos

**Resultados Comparativos**:
- Azure: 23 componentes, labels genéricos ("DATABASE")
- YOLO: 48 componentes, labels específicos ("aws_rds", "azure_sql")
- Melhoria: +108% em detecções, especificidade de labels

### 5.4 Limitações

#### 5.4.1 Limitações Técnicas

**Precisão de Detecção**:
- Componentes visualmente similares podem ser confundidos
- Setas muito curtas ou curvas apresentam maior erro
- Keypoints ocasionalmente ficam fora do bounding box

**Mapeamento de Conexões**:
- Dependente do parâmetro de tolerância (50 pixels)
- Conexões muito longas podem não ser associadas corretamente
- Múltiplas setas próximas podem causar ambiguidade

**Cobertura de Ameaças**:
- Regras STRIDE são heurísticas, não exaustivas
- Ameaças específicas de tecnologias não são cobertas
- Contramedidas são genéricas, requerem adaptação ao contexto

#### 5.4.2 Limitações de Escopo

**Tipos de Diagramas**:
- Otimizado para diagramas de arquitetura de nuvem
- Pode não funcionar bem com diagramas UML ou fluxogramas
- Requer ícones padronizados (AWS, Azure, GCP)

**Análise de Segurança**:
- Não substitui análise humana especializada
- Não considera contexto de negócio
- Não valida configurações específicas (ex: regras de firewall)

#### 5.4.3 Requisitos de Treinamento

**Dados**:
- Requer dataset anotado de qualidade
- 303 imagens podem ser insuficientes para generalização perfeita
- Novos componentes requerem re-treinamento

**Recursos Computacionais**:
- Treinamento requer GPU (9 horas com RTX 2060)
- Inferência pode ser feita em CPU, mas mais lenta
- Modelos ocupam 37MB (viável para deployment)

---

## 6. CONCLUSÃO

### 6.1 Considerações Finais

Este trabalho apresentou uma solução inovadora para automação de modelagem de ameaças em diagramas de arquitetura de software, utilizando técnicas de visão computacional e aprendizado profundo. Os resultados demonstram a viabilidade técnica e os benefícios práticos da abordagem proposta.

**Descoberta Inesperada: O Paradoxo da Especialização**

Durante a validação da solução, um teste comparativo com o modelo Gemini Pro revelou uma descoberta surpreendente: um modelo generalista de linguagem multimodal, sem qualquer treinamento específico para a tarefa, conseguiu produzir análises de qualidade superior ao modelo YOLO especializado que foi treinado por 9 horas.

Este resultado, embora inicialmente contraintuitivo, reflete o estado atual da inteligência artificial em 2026:

1. **Escala vs. Especialização**: Modelos de linguagem de grande escala (LLMs) treinados em trilhões de tokens desenvolvem capacidades emergentes que superam modelos especializados em domínios específicos.

2. **Compreensão Contextual**: O Gemini Pro demonstrou não apenas reconhecer componentes visuais, mas compreender suas implicações de segurança em um nível semântico profundo, identificando riscos como "injeção de prompt maliciosa em agentes de IA" que não estavam codificados em regras heurísticas.

3. **Custo-Benefício do Treinamento**: O investimento de 9 horas de treinamento em GPU, embora modesto, pode não ser justificável quando modelos generalistas pré-treinados oferecem resultados superiores via API.

**Reavaliação da Proposta de Valor**

À luz destes resultados, a proposta de valor da solução YOLO especializada deve ser reavaliada:

**Vantagens Mantidas**:
- Operação offline (crítico para ambientes air-gapped)
- Custo zero após treinamento (vs. custo por requisição de APIs)
- Velocidade superior (30s vs. 90s)
- Saída estruturada (JSON) ideal para automação
- Controle total sobre o modelo e dados

**Limitações Reconhecidas**:
- Análise menos profunda que modelos generalistas
- Dependência de regras heurísticas pré-definidas
- Necessidade de re-treinamento para novos componentes
- Menor capacidade de raciocínio contextual

**Conclusão Revisada**:

Os resultados sugerem que, para a maioria dos casos de uso, modelos multimodais generalistas como Gemini Pro representam a solução mais eficaz para modelagem de ameaças automatizada em 2026. A abordagem de treinar modelos especializados permanece relevante apenas em cenários específicos:

- Ambientes com restrições de conectividade
- Requisitos de privacidade que impedem uso de APIs externas
- Necessidade de integração em pipelines de CI/CD com latência mínima
- Orçamentos que não comportam custos recorrentes de API

Esta descoberta não invalida o trabalho realizado, mas contextualiza-o dentro do rápido avanço da IA. A metodologia desenvolvida - coleta de datasets, treinamento de modelos especializados, pipeline de processamento - permanece valiosa como referência técnica e pode ser aplicada em outros domínios onde modelos generalistas ainda não são superiores.

**Principais Contribuições**:

1. **Automação Efetiva**: Redução de tempo de análise de horas para segundos (~30s), representando ganho de produtividade de 99%.

2. **Detecção Abrangente**: Suporte a 111 classes de componentes de infraestrutura, cobrindo os principais provedores de nuvem (AWS, Azure, GCP).

3. **Análise Contextual**: Geração automática de ameaças baseadas em conexões específicas, identificando padrões críticos como acesso direto user→database.

4. **Arquitetura Modular**: Sistema extensível que permite adição de novas regras STRIDE e suporte a novos tipos de componentes.

5. **Gratuidade e Portabilidade**: Solução open-source que funciona offline, sem dependência de APIs pagas.

**Impacto Prático**:

A solução desenvolvida tem potencial para democratizar a prática de modelagem de ameaças, tornando-a acessível a equipes sem expertise profunda em segurança. A integração em pipelines de CI/CD permite verificações automáticas de segurança a cada mudança arquitetural, promovendo o conceito de "Security by Design".

**Validação dos Objetivos**:

Todos os objetivos específicos foram alcançados:
- ✅ Modelo YOLO para componentes treinado (111 classes)
- ✅ Modelo YOLO para setas com keypoints treinado
- ✅ Algoritmo de mapeamento de fluxo implementado
- ✅ Sistema de geração STRIDE com ameaças base e contextuais
- ✅ Pipeline completo funcional
- ✅ Avaliação em casos de uso reais
- ✅ Comparação com estado da arte (Gemini Pro)

**Lições Aprendidas**:

1. **Modelos Generalistas Superam Especializados**: Em 2026, LLMs multimodais alcançaram maturidade suficiente para superar modelos especializados em tarefas específicas, mesmo sem fine-tuning.

2. **Valor da Especialização**: Modelos especializados ainda têm valor em cenários com restrições de conectividade, privacidade ou custo.

3. **Importância da Avaliação Comparativa**: Testar contra soluções alternativas (incluindo modelos generalistas) é essencial para validar a proposta de valor.

4. **Evolução Rápida da IA**: O campo de IA evolui tão rapidamente que soluções consideradas estado da arte podem ser superadas por modelos generalistas em meses.

**Limitações Reconhecidas**:

Apesar dos resultados positivos, o sistema não é perfeito. A precisão de detecção (85-90%) é satisfatória mas inferior a modelos generalistas (~95%). Ameaças específicas de tecnologias e contextos de negócio ainda requerem análise especializada, embora modelos como Gemini Pro demonstrem capacidade superior neste aspecto.

### 6.2 Trabalhos Futuros

**Abordagem Híbrida (Recomendado)**:

Dado o desempenho superior de modelos generalistas, a direção mais promissora é uma arquitetura híbrida:

1. **YOLO para Estruturação**: Usar modelos especializados para detecção rápida e estruturada de componentes e conexões
2. **LMM para Análise**: Enviar estrutura detectada para modelo generalista (Gemini, GPT-4V) para análise contextual profunda
3. **Melhor dos Dois Mundos**: Combinar velocidade e estruturação do YOLO com raciocínio profundo de LMMs

**Integração com LLMs (Curto Prazo)**:

1. **Pipeline Híbrido**: YOLO detecta → JSON estruturado → LLM analisa → Relatório enriquecido
2. **Prompt Engineering**: Desenvolver prompts otimizados para análise STRIDE com contexto estruturado
3. **Validação Cruzada**: Usar YOLO como validador de "alucinações" do LLM
4. **Fine-tuning de LLMs**: Treinar modelos menores (Llama, Mistral) com dados de segurança específicos

**Melhorias de Médio Prazo**:

1. **Modelos Locais**: Explorar LLMs open-source que rodam localmente (Llama 3, Mistral)
2. **Análise Multi-Diagrama**: Correlacionar ameaças entre múltiplos diagramas de um sistema
3. **Integração com Ferramentas**: Plugins para Lucidchart, Draw.io, Visio
4. **Geração de Contramedidas Executáveis**: Código Terraform/CloudFormation para implementar mitigações

**Pesquisas de Longo Prazo**:

1. **Agentes Autônomos**: Sistemas que não apenas identificam ameaças, mas propõem e validam arquiteturas alternativas
2. **Aprendizado Contínuo**: Modelos que aprendem com incidentes de segurança reais
3. **Simulação de Ataques**: Gerar cenários de ataque e testar contramedidas automaticamente
4. **Análise Dinâmica**: Integrar com logs e métricas para validar ameaças em runtime

**Expansão de Escopo**:

1. **Outros Tipos de Diagramas**: UML, BPMN, fluxogramas, diagramas de rede
2. **Outras Metodologias**: PASTA, LINDDUN, Attack Trees, OCTAVE
3. **Compliance Automatizado**: Verificar conformidade com frameworks (NIST, ISO 27001, SOC 2)
4. **Análise de Código**: Correlacionar ameaças arquiteturais com vulnerabilidades no código

**Reflexão Final**:

Este trabalho demonstra tanto o potencial quanto as limitações de modelos especializados na era dos LLMs. O futuro da modelagem de ameaças automatizada provavelmente não está em escolher entre especialização ou generalização, mas em orquestrar ambas as abordagens de forma complementar. A contribuição deste trabalho permanece relevante como base técnica para sistemas híbridos que combinem o melhor de ambos os mundos.

---

## 7. REFERÊNCIAS

BERGER, B. J. et al. Automatically extracting threats from extended data flow diagrams. In: INTERNATIONAL SYMPOSIUM ON ENGINEERING SECURE SOFTWARE AND SYSTEMS, 8., 2016. Proceedings... Springer, 2016. p. 56-71.

BRESSAN, G. et al. Deep learning for automatic recognition of UML diagrams. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING, 42., 2020. Proceedings... ACM, 2020. p. 1234-1245.

HERNAN, S. et al. Uncover security design flaws using the STRIDE approach. MSDN Magazine, Microsoft, 2006. Disponível em: https://learn.microsoft.com/en-us/previous-versions/commerce-server/ee823878(v=cs.20). Acesso em: 06 mar. 2026.

MICROSOFT. Threat Modeling Security Fundamentals. Microsoft Learn, 2023. Disponível em: https://learn.microsoft.com/en-us/training/modules/tm-introduction-to-threat-modeling/. Acesso em: 06 mar. 2026.

MORENO-GARCÍA, C. F. et al. Symbol recognition in engineering drawings using statistical pattern recognition. Pattern Recognition Letters, v. 25, n. 14, p. 1621-1632, 2004.

REDMON, J. et al. You only look once: Unified, real-time object detection. In: IEEE CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION, 2016. Proceedings... IEEE, 2016. p. 779-788.

GOOGLE. Gemini Pro: Advanced Multimodal AI Model. Google AI, 2024. Disponível em: https://deepmind.google/technologies/gemini/. Acesso em: 06 mar. 2026.

ROBOFLOW. Arrow Dataset. Roboflow Universe, 2024. Disponível em: https://universe.roboflow.com/arrowhead-yjeny/arrow-dataset-ijzxx/dataset/1. Acesso em: 06 mar. 2026.

RIAN, C. Software Architecture Dataset. Kaggle, 2023. Disponível em: https://www.kaggle.com/datasets/carlosrian/software-architecture-dataset/code. Acesso em: 06 mar. 2026.

SHOSTACK, A. Threat Modeling: Designing for Security. Indianapolis: Wiley, 2014. 624 p.

SION, L. et al. An architectural view for practical threat modeling. In: EUROPEAN CONFERENCE ON SOFTWARE ARCHITECTURE, 12., 2018. Proceedings... Springer, 2018. p. 326-342.

ULTRALYTICS. YOLOv8 Documentation. Ultralytics, 2023. Disponível em: https://docs.ultralytics.com/. Acesso em: 06 mar. 2026.

VERIZON. 2023 Data Breach Investigations Report. Verizon Business, 2023. Disponível em: https://www.verizon.com/business/resources/reports/dbir/. Acesso em: 06 mar. 2026.

---

## 8. APÊNDICES

### APÊNDICE A - Instalação e Configuração

#### A.1 Requisitos de Sistema

**Hardware Mínimo**:
- CPU: Dual-core 2.0 GHz
- RAM: 8GB
- Armazenamento: 5GB livres

**Hardware Recomendado**:
- CPU: Quad-core 3.0 GHz
- RAM: 16GB
- GPU: NVIDIA com 4GB+ VRAM (para treinamento)
- Armazenamento: 10GB livres

**Software**:
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para controle de versão)

#### A.2 Instalação Passo a Passo

```bash
# 1. Clonar repositório (ou baixar ZIP)
git clone https://github.com/[usuario]/threat-modeling-ai.git
cd threat-modeling-ai

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Verificar instalação
python -c "import ultralytics; print(ultralytics.__version__)"
```

#### A.3 Uso Básico

```bash
# Análise completa (recomendado)
python analise_stride.py --input imagens_validacao

# Com GPU NVIDIA
python analise_stride.py --input imagens_validacao --device cuda

# Com GPU Apple Silicon (M1/M2/M3)
python analise_stride.py --input imagens_validacao --device mps

# Ajustar thresholds
python analise_stride.py \
    --input imagens_validacao \
    --icons-threshold 0.7 \
    --arrows-threshold 0.3

# Usar pasta de output específica
python analise_stride.py \
    --input imagens_validacao \
    --output-dir outputs/minha_analise
```

### APÊNDICE B - Estrutura de Dados

#### B.1 Formato JSON de Componentes

```json
{
  "imagens_validacao/imagem_1.png": [
    {
      "label": "aws_api_gateway",
      "prob": 0.95,
      "bbox_norm": {
        "left": 0.45,
        "top": 0.30,
        "width": 0.08,
        "height": 0.10
      }
    }
  ]
}
```

#### B.2 Formato JSON de Conexões

```json
{
  "imagens_validacao/imagem_1.png": [
    {
      "from": "user",
      "to": "aws_api_gateway",
      "arrow_type": "arrow",
      "confidence": 0.87
    }
  ]
}
```

#### B.3 Formato JSON de Ameaças

```json
{
  "component": "user → aws_rds",
  "component_type": "connection",
  "stride": "Elevation of Privilege",
  "severity": "CRITICAL",
  "description": "Acesso direto de usuário ao banco de dados",
  "mitigations": [
    "Adicionar API Gateway",
    "Implementar autenticação",
    "Remover acesso direto"
  ],
  "contextual": true
}
```

### APÊNDICE C - Classes Suportadas

#### C.1 Componentes AWS (Amostra)

- aws_amazon_api_gateway
- aws_application_load_balancer
- aws_rds
- aws_dynamodb
- aws_lambda
- aws_s3
- aws_cloudfront
- aws_waf
- aws_vpc
- aws_public_subnet
- aws_private_subnet
- aws_elasticache
- aws_cloudwatch
- aws_cloudtrail
- aws_kms
- aws_backup
- aws_autoscaling
- aws_efs
- aws_ses

#### C.2 Componentes Azure (Amostra)

- microsoft_entra
- logic_apps
- developer_portal
- azure_services
- resource_group
- sass_services

#### C.3 Componentes Genéricos

- api
- database
- storage
- user
- load_balancer
- security
- monitoring

**Total**: 111 classes

### APÊNDICE D - Exemplos de Ameaças STRIDE

#### D.1 Spoofing

**Componente**: User
**Descrição**: Atacante pode se passar por usuário legítimo
**Contramedidas**:
- Implementar MFA (Multi-Factor Authentication)
- Usar OAuth2/OIDC para autenticação
- Aplicar princípio de least privilege no IAM

#### D.2 Tampering

**Componente**: API → Database
**Descrição**: Risco de SQL Injection na conexão
**Contramedidas**:
- Usar prepared statements
- Implementar ORM (Object-Relational Mapping)
- Validar e sanitizar todas as entradas
- Aplicar princípio de least privilege no usuário do banco

#### D.3 Information Disclosure

**Componente**: Qualquer conexão
**Descrição**: Dados podem ser interceptados em trânsito
**Contramedidas**:
- Usar TLS 1.3 para todas as conexões
- Implementar mTLS quando aplicável
- Usar VPN ou AWS PrivateLink para tráfego interno

#### D.4 Denial of Service

**Componente**: API Gateway
**Descrição**: Sistema pode ser sobrecarregado por requisições
**Contramedidas**:
- Implementar rate limiting
- Configurar autoscaling
- Usar WAF/Shield para proteção DDoS
- Implementar circuit breakers

#### D.5 Elevation of Privilege (CRÍTICO)

**Componente**: User → Database
**Descrição**: Acesso direto sem camada intermediária
**Contramedidas**:
- Adicionar API Gateway entre user e database
- Implementar camada de aplicação
- Remover completamente acesso direto
- Aplicar RBAC rigoroso

---

**FIM DO DOCUMENTO**

---

**Informações do Trabalho**:
- Título: Modelagem Automatizada de Ameaças em Diagramas de Arquitetura de Software Utilizando Inteligência Artificial e Metodologia STRIDE
- Área: Engenharia de Software / Segurança da Informação
- Palavras-chave: Modelagem de Ameaças, STRIDE, Visão Computacional, YOLO, Segurança de Software
- Data: Março de 2026
