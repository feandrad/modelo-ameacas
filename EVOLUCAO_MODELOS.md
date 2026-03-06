# 📊 Evolução dos Modelos - Azure vs YOLO

## Jornada do Projeto

### Fase 1: Azure Custom Vision (Prova de Conceito)

**Objetivo**: Validar viabilidade de detecção automática

**Implementação**:
- Treinamento com dataset de diagramas AWS
- Modelo cloud (Azure Custom Vision)
- ~10 classes genéricas

**Resultados**:
- ✅ Provou que IA pode detectar componentes
- ✅ Gerou relatório STRIDE básico
- ❌ Labels genéricos (DATABASE, API, VPC)
- ❌ Custo por requisição
- ❌ Dependência de internet
- ❌ Apenas 23 componentes detectados

### Fase 2: YOLO Local (Produção)

**Objetivo**: Escalar solução com mais precisão e zero custo

**Implementação**:
- 2 modelos YOLO especializados
- best_icons.pt: 111 classes (AWS/Azure/GCP)
- best_arrows.pt: Setas com keypoints

**Resultados**:
- ✅ 42 componentes detectados (+83%)
- ✅ Labels específicos (aws_rds, azure_sql, gcp_bigquery)
- ✅ Gratuito (sem custo de API)
- ✅ Offline (não precisa internet)
- ✅ Multi-cloud (3 providers)
- ✅ Keypoints nas setas (direção real)

---

## Comparação Técnica

| Métrica | Azure Custom Vision | YOLO Local | Melhoria |
|---------|---------------------|------------|----------|
| **Componentes detectados** | 23 | 42 | +83% |
| **Classes disponíveis** | ~10 | 111 | +1010% |
| **Clouds suportados** | 1 (AWS) | 3 (AWS/Azure/GCP) | +200% |
| **Custo por análise** | $0.10 | $0.00 | -100% |
| **Requer internet** | Sim | Não | ✅ |
| **Detecção de setas** | Não | Sim (keypoints) | ✅ |
| **Labels** | Genéricos | Específicos | ✅ |

---

## Exemplo Prático

### Mesmo Componente, Labels Diferentes

**Azure Custom Vision**:
```json
{
  "label": "DATABASE",
  "prob": 0.82
}
```

**YOLO Local**:
```json
{
  "label": "aws_rds",
  "prob": 0.85
}
```

**Impacto no STRIDE**:
- Azure: Ameaças genéricas para "DATABASE"
- YOLO: Ameaças específicas para "aws_rds" (ex: backup automático, Multi-AZ, etc)

---

## Por Que 0% de Match?

Rodamos comparação entre os dois modelos:

```bash
python scripts/comparar_modelos_icons.py
```

**Resultado**:
- Match: 0%
- Precision: 0.00%
- Recall: 0.00%

**Motivos**:
1. **Labels incompatíveis**: "DATABASE" ≠ "aws_rds"
2. **Granularidade diferente**: Azure genérico, YOLO específico
3. **Bounding boxes diferentes**: Posições não coincidem

**Conclusão**: Não são complementares, são substitutos.

---

## Decisão: Migrar para YOLO

### Critérios de Decisão

1. **Custo**: $0 vs $0.10 por análise
2. **Precisão**: 42 vs 23 componentes
3. **Especificidade**: aws_rds vs DATABASE
4. **Escalabilidade**: Offline vs API rate limits
5. **Multi-cloud**: 3 clouds vs 1 cloud
6. **Inovação**: Keypoints nas setas

### Resultado

✅ **YOLO venceu em todos os critérios**

---

## Lições Aprendidas

### O que funcionou

1. **Azure foi ótimo para MVP**: Validou conceito rapidamente
2. **Dataset reutilizável**: Mesmo dataset treinou ambos modelos
3. **Migração suave**: Mantivemos mesma interface (JSON)

### O que melhoramos

1. **Labels específicos**: Melhor análise STRIDE
2. **Detecção de setas**: Análise de fluxo
3. **Keypoints**: Direção real das conexões
4. **Multi-cloud**: Não limitado a AWS

### Próximos Passos

1. ✅ Modelo de setas com keypoints
2. ✅ Análise STRIDE contextual
3. 🔄 Detecção de protocolos (HTTP, SQL, etc)
4. 🔄 Análise de trust boundaries
5. 🔄 Grafo de dependências

---

## Para a Apresentação

### Mensagem Principal

"Começamos com Azure Custom Vision para validar o conceito. Funcionou, mas tinha limitações. Migramos para YOLO local e conseguimos 83% mais detecções, labels específicos para 3 clouds, e tudo isso gratuitamente e offline."

### Pontos-Chave

1. **Evolução natural**: MVP → Produção
2. **Decisão baseada em dados**: Comparação objetiva
3. **Resultado superior**: Mais detecções, mais específico, gratuito
4. **Inovação**: Keypoints nas setas (diferencial)

### Demo Sugerida

1. Mostrar `comparacao_modelos.md` (0% match)
2. Explicar por que labels diferentes
3. Rodar `analise_stride.py` com YOLO
4. Mostrar resultado superior

---

## Métricas de Sucesso

### Antes (Azure)
- 23 componentes
- 10 classes
- $0.10/análise
- 1 cloud

### Depois (YOLO)
- 42 componentes (+83%)
- 111 classes (+1010%)
- $0.00/análise (-100%)
- 3 clouds (+200%)

**ROI**: Infinito (custo zero com resultado superior)
