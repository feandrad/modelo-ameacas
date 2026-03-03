import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

EXTS = {".png", ".jpg", ".jpeg", ".webp"}


# ---------------------------
# Utilidades
# ---------------------------
def serialize_polygon(polygon):
    """Converte lista de ImagePoint para lista serializável [{x,y}, ...]."""
    if not polygon:
        return []
    return [{"x": getattr(p, "x", None), "y": getattr(p, "y", None)} for p in polygon]


def find_images(input_dir: Path, recursive: bool) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {input_dir.resolve()}")

    it = input_dir.rglob("*") if recursive else input_dir.glob("*")
    images = sorted([p for p in it if p.is_file() and p.suffix.lower() in EXTS])

    if not images:
        raise FileNotFoundError(f"Nenhuma imagem encontrada em: {input_dir.resolve()}")

    return images


def ensure_parent_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------
# Azure client
# ---------------------------
def build_client_from_env() -> ImageAnalysisClient:
    load_dotenv()

    key = os.getenv("KEY_VISION")
    endpoint = os.getenv("ENDPOINT_VISION")

    if not key or not endpoint:
        raise RuntimeError(
            "Faltam variáveis no .env. Necessário:\n"
            "KEY=...\n"
            "ENDPOINT=https://<seu-recurso>.cognitiveservices.azure.com/"
        )

    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


# ---------------------------
# OCR por imagem
# ---------------------------
def ocr_one_image(client: ImageAnalysisClient, img_path: Path) -> dict:
    """
    Retorna um dict padronizado:
    {
      "status": "ok" | "error",
      "lines": [{"text": "...", "bbox": [...]}, ...],
      "error": "..." (se status=error)
    }
    """
    try:
        with open(img_path, "rb") as f:
            result = client.analyze(
                image_data=f,
                visual_features=[VisualFeatures.READ],
                gender_neutral_caption=True,
            )

        lines_out = []
        if result.read and result.read.blocks:
            for block in result.read.blocks:
                for line in block.lines:
                    lines_out.append(
                        {
                            "text": line.text,
                            "bbox": serialize_polygon(line.bounding_polygon),
                        }
                    )

        return {"status": "ok", "lines": lines_out}

    except Exception as e:
        return {"status": "error", "lines": [], "error": str(e)}


# ---------------------------
# OCR pasta inteira
# ---------------------------
def ocr_folder(client: ImageAnalysisClient, images: list[Path]) -> dict:
    items = {}
    ok = 0
    err = 0
    total_lines = 0

    for i, img_path in enumerate(images, start=1):
        key = img_path.as_posix()
        payload = ocr_one_image(client, img_path)
        items[key] = payload

        if payload["status"] == "ok":
            ok += 1
            n = len(payload["lines"])
            total_lines += n
            print(f"[{i}/{len(images)}] OK  - {img_path.name} | linhas: {n}")
        else:
            err += 1
            print(f"[{i}/{len(images)}] ERRO- {img_path.name} | {payload.get('error')}")

    return {
        "meta": {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "images_total": len(images),
            "images_ok": ok,
            "images_error": err,
            "lines_total": total_lines,
        },
        "items": items,
    }


# ---------------------------
# CLI
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="OCR (Azure AI Vision - READ) em uma pasta de imagens.")
    parser.add_argument("--input", type=str, default="data/dataset_imagens", help="Pasta com imagens")
    parser.add_argument("--out", type=str, default="data/ocr/ocr_result.json", help="Arquivo JSON de saída")
    parser.add_argument("--no-recursive", action="store_true", help="Não buscar em subpastas")
    args = parser.parse_args()

    input_dir = Path(args.input)
    out_file = Path(args.out)
    recursive = not args.no_recursive

    client = build_client_from_env()
    images = find_images(input_dir, recursive=recursive)

    print(f"Imagens encontradas: {len(images)}")
    result = ocr_folder(client, images)

    ensure_parent_dir(out_file)
    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)

    print(f"\nOCR salvo em: {out_file.as_posix()}")
    print(f"Resumo: {result['meta']}")


if __name__ == "__main__":
    main()