# Projeto de Modelagem de Ameacas com OCR + Custom Vision + STRIDE

Este projeto processa diagramas de arquitetura em imagem, extrai texto, mapeia componentes, treina/detecta com Azure Custom Vision e gera um relatorio final de ameacas no modelo STRIDE.

## Pre-requisitos

- Python 3.10+
- Ambiente virtual (recomendado)
- Dependencias do `requirements.txt`
- Conta Azure com:
  - Azure AI Vision (OCR)
  - Azure Custom Vision (Training + Prediction)

## Instalacao

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuracao de ambiente

Crie um arquivo `.env` na raiz do projeto com:

```env
# OCR (Azure AI Vision)
KEY_VISION=...
ENDPOINT_VISION=https://<seu-recurso>.cognitiveservices.azure.com/

# Custom Vision - Training
KEY_TRAINING=...
ENDPOINT_TRAINING=https://<seu-training-endpoint>.cognitiveservices.azure.com/

# Custom Vision - Prediction
PREDICTION_KEY=...
PREDICTION_ENDPOINT=https://<seu-prediction-endpoint>.cognitiveservices.azure.com/
PREDICTION_NAME=<nome_publicado_do_modelo>

# Projeto Custom Vision
PROJECT_ID_VISION=<uuid-do-projeto>
```

## Sequencia de execucao

Execute os scripts na ordem abaixo.

1. Extrair texto das imagens (OCR)

```bash
python scripts/extrair_texto_img.py
```

Saida padrao: `data/ocr/ocr_result.json`

2. Mapear componentes a partir do OCR

```bash
python scripts/mapeamento_componentes.py
```

Saidas padrao:
- `data/components_output/components_candidates.json`
- `data/components_output/components_review.json`

3. Gerar rastreabilidade visual de bounding boxes

```bash
python scripts/rastreabilidade_boxs.py
```

Saida padrao: `outputs/boxs_overlays/`

4. Subir dataset rotulado para treino no Custom Vision

```bash
python scripts/upload_to_custom_vision.py
```

Opcional (simulacao sem upload):

```bash
python scripts/upload_to_custom_vision.py --dry-run
```

5. Detectar componentes com modelo publicado

```bash
python scripts/detectar_componentes.py
```

Saida padrao: `data/predictions/predictions.json`

6. Gerar relatorio STRIDE

```bash
python scripts/gerar_relatorio_stride.py
```

Saidas padrao:
- `outputs/reports/relatorio_final.md`
- `data/modelo_ameacas/threat_model.json`


