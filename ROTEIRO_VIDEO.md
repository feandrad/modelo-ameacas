# 🎬 Roteiro de Vídeo - Modelagem de Ameaças com IA (15 min)

## 📋 Estrutura do Vídeo

**Duração total**: 15 minutos
**Formato**: Demonstração prática + explicação técnica

---

## 🎯 INTRODUÇÃO (2 min)

### Slide 1: Problema
**[0:00 - 0:30]**
- "Arquitetos de software criam diagramas de arquitetura todos os dias"
- "Mas fazer modelagem de ameaças manualmente é demorado e propenso a erros"
- "E se pudéssemos automatizar isso usando IA?"

### Slide 2: Solução
**[0:30 - 1:00]**
- "Desenvolvemos um sistema que analisa diagramas automaticamente"
- "Detecta componentes, mapeia conexões e gera relatório STRIDE"
- "Tudo isso em segundos"

### Slide 3: Tecnologias
**[1:00 - 2:00]**
- **2 Modelos YOLO**:
  - best_icons.pt: 111 tipos de componentes (AWS/Azure/GCP)
  - best_arrows.pt: Detecção de setas/conexões
- **Metodologia STRIDE**: Framework da Microsoft para análise de ameaças
- **Python + Ultralytics**: Stack de desenvolvimento

---

## 🏗️ ARQUITETURA DA SOLUÇÃO (3 min)

### Evolução do Projeto
**[2:00 - 3:00]**

**Versão 1: Azure Custom Vision**
- Começamos com Azure Custom Vision (cloud)
- Treinamos modelo com dataset de diagramas
- Detectava ~10 classes genéricas (API, DATABASE, etc)
- **Limitações**:
  - Custo de API por requisição
  - Labels genéricos demais
  - Dependência de internet
  - Menos detecções (23 componentes)

**Versão 2: YOLO Local (Atual)**
- Migramos para YOLO (ultralytics)
- 2 modelos especializados:
  - best_icons.pt: 111 classes (AWS/Azure/GCP)
  - best_arrows.pt: Detecção de setas com keypoints
- **Vantagens**:
  - ✅ Gratuito (sem custo de API)
  - ✅ Offline (não precisa internet)
  - ✅ Mais preciso (42 vs 23 componentes)
  - ✅ Labels específicos (aws_rds, azure_sql, gcp_bigquery)
  - ✅ Keypoints nas setas (direção real)

### Comparação Lado a Lado
**[3:00 - 5:00]**

**Mostrar arquivo: comparacao_modelos.md**

```
Azure Custom Vision:
- 23 componentes detectados
- Labels: API_GATEWAY, DATABASE, VPC
- Match com YOLO: 0%

YOLO Local:
- 42 componentes detectados  
- Labels: aws_application_load_balancer, aws_rds, azure_sql
- 111 classes (AWS + Azure + GCP)
```

**Por que 0% de match?**
- Labels completamente diferentes
- Azure: genérico (DATABASE)
- YOLO: específico (aws_rds, azure_sql, gcp_cloud_sql)

**Decisão: Seguir com YOLO**
- Mais detecções
- Mais específico
- Gratuito
- Suporta 3 clouds

---

## 💻 DEMONSTRAÇÃO PRÁTICA (7 min)

### Demo 1: Mostrar Evolução
**[5:00 - 6:30]**

**Arquivo: comparacao_modelos.md**
```bash
cat outputs/reports/comparacao_modelos.md
```

**Narração**:
- "Começamos com Azure Custom Vision"
- "Detectou 23 componentes, mas com labels genéricos"
- "Migramos para YOLO local"
- "Agora detecta 42 componentes com labels específicos"
- "E o melhor: é gratuito e funciona offline"

### Demo 2: Executar Pipeline YOLO
**[6:30 - 8:30]**

```bash
python analise_stride.py
```

**Narração enquanto executa**:
- "Vou executar o pipeline completo com YOLO"
- "Etapa 1: Detectando componentes... 49 encontrados"
- "Etapa 2: Detectando setas... 45 encontradas"
- "Etapa 3: Mapeando conexões... 7 conexões identificadas"
- "Etapa 4: Gerando relatório STRIDE..."

### Demo 3: Mostrar Resultados
**[8:30 - 10:00]**

**Arquivo 1: predictions_yolo.json**
```json
{
  "label": "aws_application_load_balancer",
  "prob": 0.85,
  "bbox_norm": {...}
}
```
- "Aqui temos todos os componentes detectados"
- "Cada um com sua confiança e posição"

**Arquivo 2: connections.json**
```json
{
  "from": "aws_public_subnet",
  "to": "aws_cloudfront",
  "confidence": 0.77
}
```
- "E aqui as conexões mapeadas"
- "Subnet pública conecta com CloudFront"

**Arquivo 3: stride_completo.md**
- "E finalmente o relatório STRIDE"
- "Veja aqui: 23 ameaças base + 3 contextuais"

### Demo 4: Ameaças Contextuais
**[10:00 - 12:00]**

**Mostrar exemplo real do relatório**:

```markdown
### 🚨 AMEAÇAS CRÍTICAS
#### Elevation of Privilege: Acesso direto de usuário ao banco
**Componente**: USER → DATABASE
**Contramedidas**:
- Adicionar API Gateway
- Implementar camada de aplicação
```

**Explicar**:
- "Esta é uma ameaça contextual - só detectada porque analisamos o FLUXO"
- "Se fosse só análise de componentes, não veríamos esse problema"
- "O sistema detectou que usuário acessa banco direto - isso é CRÍTICO"

**Outro exemplo**:
```markdown
🟠 HIGH: Risco de SQL Injection na conexão API-Database
```
- "Aqui detectou API conectando com banco"
- "Automaticamente sugere prepared statements e validação"

---

## 📊 RESULTADOS E MÉTRICAS (2 min)

### Slide: Estatísticas
**[12:00 - 13:00]**

**Nas 3 imagens de teste**:
- ✅ 49 componentes detectados
- ✅ 45 setas detectadas
- ✅ 7 conexões mapeadas
- ✅ 48 ameaças identificadas
- ⚡ Tempo total: ~30 segundos

**Comparação manual vs automático**:
- Manual: 2-4 horas por diagrama
- Automático: 30 segundos
- **Ganho: 240x mais rápido**

### Slide: Tipos de Ameaças
**[13:00 - 14:00]**

**Ameaças Base** (por componente):
- Spoofing, Tampering, Repudiation
- Information Disclosure, DoS
- Elevation of Privilege

**Ameaças Contextuais** (por conexão):
- USER → DATABASE direto
- API → DATABASE sem validação
- Conexões sem criptografia
- Exposição sem WAF

---

## 🎓 CONCLUSÃO (1 min)

### Slide: Diferenciais
**[14:00 - 14:30]**

1. **Evolução Azure → YOLO**: Mostramos a jornada e decisão técnica
2. **Dupla análise**: Componentes (111 classes) + Conexões (keypoints)
3. **Multi-cloud**: AWS, Azure, GCP em um único modelo
4. **Ameaças contextuais**: Baseadas no fluxo real de dados
5. **Open source**: Gratuito, offline, sem vendor lock-in

### Slide: Próximos Passos
**[14:30 - 15:00]**

- 🔄 Detecção de protocolos (HTTP, SQL, etc)
- 🎯 Análise de trust boundaries
- 📈 Grafo de dependências
- 🤖 Sugestões automáticas de correção

**Encerramento**:
- "Código disponível no GitHub"
- "Obrigado!"

---

## 🎥 DICAS DE GRAVAÇÃO

### Preparação
- [ ] Ter 3 imagens de teste prontas
- [ ] Pipeline já executado uma vez (para ser rápido)
- [ ] Relatório stride_completo.md aberto
- [ ] Terminal com fonte grande e legível
- [ ] Slides preparados (máximo 5 slides)

### Durante a Gravação
- **Ritmo**: Falar devagar e claro
- **Pausas**: Dar tempo para processar informação
- **Zoom**: Aumentar fonte do terminal
- **Destaque**: Usar cursor para apontar partes importantes
- **Energia**: Manter tom entusiasmado mas profissional

### Estrutura de Tempo
```
0:00 - 2:00  → Introdução (problema + solução)
2:00 - 5:00  → Arquitetura (como funciona)
5:00 - 12:00 → Demo prática (executar + mostrar)
12:00 - 14:00 → Resultados (métricas + comparação)
14:00 - 15:00 → Conclusão (diferenciais + próximos passos)
```

### Checklist Final
- [ ] Áudio limpo (sem ruído de fundo)
- [ ] Tela em HD (1920x1080 mínimo)
- [ ] Fonte do terminal legível
- [ ] Não ultrapassar 15 minutos
- [ ] Mostrar código funcionando (não só slides)
- [ ] Explicar STRIDE brevemente
- [ ] Destacar ameaças contextuais (diferencial)

---

## 📝 SCRIPT DETALHADO

### Abertura (palavra por palavra)

"Olá! Sou [NOME] e vou apresentar nosso projeto de Modelagem de Ameaças Automatizada usando Inteligência Artificial.

O problema que resolvemos é simples: arquitetos de software passam horas fazendo análise de segurança manualmente. E se pudéssemos automatizar isso?

Nossa solução usa dois modelos de IA treinados especificamente para isso. O primeiro detecta componentes - APIs, bancos de dados, load balancers. O segundo detecta as conexões entre eles. E com essas duas informações, geramos um relatório STRIDE completo, identificando ameaças que um humano levaria horas para encontrar.

Vamos ver como funciona..."

### Durante a Demo

"Vou executar o pipeline completo. [EXECUTAR]

Olha só... em poucos segundos ele já detectou 31 componentes nesta imagem. API Gateway, Load Balancer, RDS, VPC...

Agora está detectando as setas... 5 setas encontradas. E o mais importante: ele está MAPEANDO as conexões. Ou seja, ele sabe que a subnet pública conecta com o CloudFront, que conecta com o WAF.

E é aqui que fica interessante. [ABRIR RELATÓRIO]

Veja esta ameaça crítica: 'Acesso direto de usuário ao banco de dados'. O sistema detectou isso porque ele ANALISOU O FLUXO. Se fosse só olhar componentes isolados, não veria esse problema.

Isso é o diferencial: ameaças contextuais baseadas em como os componentes se conectam."

### Fechamento

"Em resumo: desenvolvemos um sistema que em 30 segundos faz o que um humano levaria horas. Detecta componentes, mapeia conexões e gera ameaças contextuais.

O código está disponível no GitHub. Obrigado!"

---

## 🎬 ALTERNATIVA: Roteiro Curto (10 min)

Se precisar encurtar:

**Cortar**:
- Explicação detalhada de STRIDE (assumir que conhecem)
- Comparação com Azure Custom Vision
- Detalhes técnicos de threshold

**Manter**:
- Demo prática (essencial)
- Ameaças contextuais (diferencial)
- Resultados (impacto)
