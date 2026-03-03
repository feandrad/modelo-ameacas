import os
import json
import argparse
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateEntry,
    ImageFileCreateBatch,
    Region,
)

# ---------------------------
# Paths defaults (mude via CLI)
# ---------------------------
DEFAULT_CANDIDATES = "data/components_output/components_candidates.json"
DEFAULT_IMAGES_ROOT = "data/dataset_imagens"


# ---------------------------
# Config / Client
# ---------------------------
def load_env():
    load_dotenv()
    key = os.getenv("KEY_TRAINING")
    endpoint = os.getenv("ENDPOINT_TRAINING")
    project_id = os.getenv("PROJECT_ID_VISION")

    missing = [n for n, v in [("KEY_TRAINING", key), ("ENDPOINT_TRAINING", endpoint), ("PROJECT_ID_VISION", project_id)] if not v]
    if missing:
        raise RuntimeError("Configure no .env: " + ", ".join(missing))

    return key, endpoint, project_id


def build_trainer(training_key: str, endpoint: str) -> CustomVisionTrainingClient:
    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
    return CustomVisionTrainingClient(endpoint, credentials)


# ---------------------------
# IO helpers
# ---------------------------
def resolve_image_path(img_key: str, images_root: Path) -> Path:
    """
    img_key pode ser path completo ou só nome do arquivo.
    """
    p = Path(img_key)
    if p.exists():
        return p
    return images_root / p.name


def read_candidates(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Não achei candidates JSON: {path.resolve()}")
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------
# Custom Vision helpers
# ---------------------------
def get_or_create_tag(trainer, project_id: str, tag_map: dict, label: str):
    """
    label: "database" -> cria/usa tag "DATABASE"
    """
    label_key = label.strip().lower()
    label_for_cv = label_key.upper()

    if label_key in tag_map:
        return tag_map[label_key]

    tag = trainer.create_tag(project_id, label_for_cv)
    tag_map[label_key] = tag
    print(f"  + Tag criada: {label_for_cv}")
    return tag


def bbox_to_region(tag_id, bbox, img_w: int, img_h: int):
    """
    bbox: [x1,y1,x2,y2] em pixels
    Custom Vision pede valores normalizados (0..1)
    """
    if not bbox or len(bbox) != 4:
        return None

    x1, y1, x2, y2 = bbox

    # validações básicas
    if x2 <= x1 or y2 <= y1:
        return None
    if img_w <= 0 or img_h <= 0:
        return None

    left = x1 / img_w
    top = y1 / img_h
    width = (x2 - x1) / img_w
    height = (y2 - y1) / img_h

    # clamp simples pra evitar valores fora (alguns OCRs dão pequenas extrapolações)
    left = max(0.0, min(1.0, left))
    top = max(0.0, min(1.0, top))
    width = max(0.0, min(1.0 - left, width))
    height = max(0.0, min(1.0 - top, height))

    if width <= 0 or height <= 0:
        return None

    return Region(tag_id=tag_id, left=left, top=top, width=width, height=height)


def upload_one_image(trainer, project_id: str, img_path: Path, regions: list, dry_run: bool):
    """
    Envia 1 imagem com várias regiões.
    """
    if dry_run:
        print(f"  (dry-run) Enviaria: {img_path.name} | regions: {len(regions)}")
        return True

    with open(img_path, "rb") as f:
        image_data = f.read()

    entry = ImageFileCreateEntry(
        name=img_path.name,
        contents=image_data,
        regions=regions,
    )

    batch = ImageFileCreateBatch(images=[entry])
    result = trainer.create_images_from_files(project_id, batch)

    if not result.is_batch_successful:
        print("  ! Falha no upload:", result)
        return False

    return True


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Upload de imagens + bounding boxes para Custom Vision (Object Detection).")
    parser.add_argument("--candidates", type=str, default=DEFAULT_CANDIDATES, help="JSON com label/text/bbox")
    parser.add_argument("--images-root", type=str, default=DEFAULT_IMAGES_ROOT, help="Pasta com as imagens originais")
    parser.add_argument("--limit", type=int, default=0, help="Limita quantas imagens enviar (0 = todas)")
    parser.add_argument("--dry-run", action="store_true", help="Não envia nada, só imprime o que faria")
    args = parser.parse_args()

    training_key, endpoint, project_id = load_env()
    trainer = build_trainer(training_key, endpoint)

    candidates_path = Path(args.candidates)
    images_root = Path(args.images_root)

    data = read_candidates(candidates_path)

    # tags existentes
    existing_tags = trainer.get_tags(project_id)
    tag_map = {t.name.strip().lower(): t for t in existing_tags}
    print("Tags existentes:", [t.name for t in existing_tags])

    total_imgs = 0
    sent_ok = 0
    sent_err = 0
    skipped_empty = 0
    skipped_missing = 0
    skipped_no_regions = 0

    items_list = list(data.items())
    if args.limit and args.limit > 0:
        items_list = items_list[: args.limit]

    for img_key, objs in items_list:
        total_imgs += 1

        if not objs:
            skipped_empty += 1
            continue

        img_path = resolve_image_path(img_key, images_root)
        if not img_path.exists():
            print(f"[{total_imgs}] Imagem não encontrada: {img_key} -> {img_path.as_posix()}")
            skipped_missing += 1
            continue

        # tamanho da imagem
        with Image.open(img_path) as im:
            w, h = im.size

        regions = []
        for obj in objs:
            label = obj.get("label")
            bbox = obj.get("bbox")

            if not label:
                continue

            tag = get_or_create_tag(trainer, project_id, tag_map, label)
            region = bbox_to_region(tag.id, bbox, w, h)
            if region:
                regions.append(region)

        if not regions:
            print(f"[{total_imgs}] Sem regiões válidas: {img_path.name} (bbox inválida ou vazia)")
            skipped_no_regions += 1
            continue

        print(f"[{total_imgs}] Upload: {img_path.name} | regions: {len(regions)}")
        ok = upload_one_image(trainer, project_id, img_path, regions, dry_run=args.dry_run)

        if ok:
            sent_ok += 1
        else:
            sent_err += 1

    print("\n=== RESUMO ===")
    print("Total analisadas:", total_imgs)
    print("Enviadas OK:", sent_ok)
    print("Enviadas com erro:", sent_err)
    print("Puladas (sem objs):", skipped_empty)
    print("Puladas (imagem faltando):", skipped_missing)
    print("Puladas (sem regiões válidas):", skipped_no_regions)
    print("Dry-run:", args.dry_run)


if __name__ == "__main__":
    main()