import os
import io
import json
import argparse
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from PIL import Image

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials


# ---------------------------
# Constantes
# ---------------------------
EXTS = {".png", ".jpg", ".jpeg", ".webp"}
MAX_BYTES = 4 * 1024 * 1024  # 4MB (limite típico do Custom Vision Prediction)


# ---------------------------
# Config / Client
# ---------------------------
def load_env():
    load_dotenv()

    pred_key = os.getenv("PREDICTION_KEY")
    pred_endpoint = os.getenv("PREDICTION_ENDPOINT")
    project_id = os.getenv("PROJECT_ID_VISION")
    published_name = os.getenv("PREDICTION_NAME")

    missing = [n for n, v in [
        ("PREDICTION_KEY", pred_key),
        ("PREDICTION_ENDPOINT", pred_endpoint),
        ("PROJECT_ID_VISION", project_id),
        ("PREDICTION_NAME", published_name),
    ] if not v]

    if missing:
        raise RuntimeError("Faltam variáveis no .env: " + ", ".join(missing))

    return pred_key, pred_endpoint, project_id, published_name


def build_predictor(pred_key: str, pred_endpoint: str) -> CustomVisionPredictionClient:
    creds = ApiKeyCredentials(in_headers={"Prediction-key": pred_key})
    return CustomVisionPredictionClient(pred_endpoint, creds)


# ---------------------------
# IO helpers
# ---------------------------
def list_images(input_dir: Path, recursive: bool = True) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {input_dir.resolve()}")

    it = input_dir.rglob("*") if recursive else input_dir.glob("*")
    images = sorted([p for p in it if p.is_file() and p.suffix.lower() in EXTS])

    if not images:
        raise FileNotFoundError(f"Nenhuma imagem encontrada em: {input_dir.resolve()}")

    return images


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


# ---------------------------
# Image bytes (com compressão se necessário)
# ---------------------------
def compress_to_under_4mb(path: Path) -> bytes:
    """
    Lê bytes da imagem. Se passar de 4MB, converte para JPEG e reduz tamanho/qualidade
    até ficar abaixo do limite.
    """
    raw = path.read_bytes()
    if len(raw) <= MAX_BYTES:
        return raw

    img = Image.open(path).convert("RGB")  # JPEG não suporta alpha

    target_widths = [2200, 1800, 1600, 1280, 1024]
    qualities = [90, 85, 80, 75, 70, 60]

    last_data = None

    for tw in target_widths:
        w, h = img.size
        if w > tw:
            new_h = int(h * (tw / w))
            resized = img.resize((tw, new_h))
        else:
            resized = img

        for q in qualities:
            buf = io.BytesIO()
            resized.save(buf, format="JPEG", quality=q, optimize=True)
            data = buf.getvalue()
            last_data = data

            if len(data) <= MAX_BYTES:
                return data

    # fallback: melhor tentativa (menor) pra evitar crash
    return last_data if last_data is not None else raw


# ---------------------------
# Prediction
# ---------------------------
def run_prediction_on_image(predictor, project_id: str, published_name: str, img_bytes: bytes, threshold: float):
    """
    Retorna lista de detecções filtradas por threshold.
    bbox_norm é (0..1) no formato left/top/width/height.
    """
    preds = predictor.detect_image(project_id, published_name, img_bytes)

    keep = []
    for p in preds.predictions:
        prob = float(p.probability)
        if prob < threshold:
            continue

        bb = p.bounding_box
        keep.append({
            "label": p.tag_name,
            "prob": prob,
            "bbox_norm": {
                "left": float(bb.left),
                "top": float(bb.top),
                "width": float(bb.width),
                "height": float(bb.height),
            }
        })

    return keep


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Inferência (Prediction) usando Azure Custom Vision Object Detection.")
    parser.add_argument("--input", type=str, default="data/imagens_validacao", help="Pasta com imagens para prever")
    parser.add_argument("--out", type=str, default="data/predictions/predictions.json", help="JSON de saída")
    parser.add_argument("--threshold", type=float, default=0.5, help="Probabilidade mínima (0-1)")
    parser.add_argument("--no-recursive", action="store_true", help="Não buscar imagens em subpastas")
    parser.add_argument("--limit", type=int, default=0, help="Limita quantas imagens processar (0 = todas)")
    parser.add_argument("--dry-run", action="store_true", help="Não chama API, só testa leitura/compressão")
    args = parser.parse_args()

    input_dir = Path(args.input)
    out_file = Path(args.out)
    ensure_dir(out_file.parent)

    images = list_images(input_dir, recursive=not args.no_recursive)
    if args.limit and args.limit > 0:
        images = images[: args.limit]

    pred_key, pred_endpoint, project_id, published_name = load_env()
    predictor = build_predictor(pred_key, pred_endpoint)

    results = {}
    failed = 0
    total_kept = 0

    for i, img_path in enumerate(images, start=1):
        try:
            img_bytes = compress_to_under_4mb(img_path)

            if args.dry_run:
                results[img_path.as_posix()] = []
                print(f"[{i}/{len(images)}] DRY  - {img_path.name} | bytes: {len(img_bytes)}")
                continue

            dets = run_prediction_on_image(
                predictor=predictor,
                project_id=project_id,
                published_name=published_name,
                img_bytes=img_bytes,
                threshold=args.threshold,
            )

            results[img_path.as_posix()] = dets
            total_kept += len(dets)
            print(f"[{i}/{len(images)}] OK   - {img_path.name} | dets: {len(dets)}")

        except Exception as e:
            failed += 1
            results[img_path.as_posix()] = []
            print(f"[{i}/{len(images)}] ERRO - {img_path.name}: {e}")

    payload = {
        "meta": {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "input_dir": input_dir.as_posix(),
            "images_total": len(images),
            "failed": failed,
            "threshold": args.threshold,
            "published_name": published_name,
            "project_id": project_id,
            "dry_run": args.dry_run,
            "detections_total": total_kept,
        },
        "items": results,
    }

    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n=== RESUMO ===")
    print("Salvo:", out_file.as_posix())
    print("Imagens processadas:", len(images))
    print("Falhas:", failed)
    print("Detecções totais:", total_kept)


if __name__ == "__main__":
    main()