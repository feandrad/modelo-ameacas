import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------
# Visual helpers
# ---------------------------
def load_font(size=22):
    """
    Tenta carregar Arial (Windows). Se não existir, usa fonte padrão.
    """
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def resolve_image_path(img_key: str, images_root: Path) -> Path:
    """
    img_key pode vir como:
      - path completo (existente na máquina)
      - path relativo (data/dataset_imagens/xxx.png)
      - só o nome do arquivo (xxx.png)

    Estratégia:
      1) se img_key existe como path -> usa
      2) tenta images_root / img_key (se img_key for relativo)
      3) tenta images_root / nome_do_arquivo
    """
    p = Path(img_key)

    if p.exists():
        return p

    # tenta como relativo ao root
    p2 = images_root / p.as_posix()
    if p2.exists():
        return p2

    # fallback: só o nome
    p3 = images_root / p.name
    return p3


def draw_label(draw: ImageDraw.ImageDraw, x1: int, y1: int, text: str, font):
    """
    Desenha uma tarja preta com texto branco próximo do bbox.
    """
    pad = 4
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]

    # tenta desenhar acima; se não couber, desenha abaixo
    ly2 = y1
    ly1 = y1 - th - 2 * pad
    if ly1 < 0:
        ly1 = y1
        ly2 = y1 + th + 2 * pad

    lx1 = x1
    lx2 = x1 + tw + 2 * pad

    draw.rectangle([lx1, ly1, lx2, ly2], fill="black")
    draw.text((lx1 + pad, ly1 + pad), text, font=font, fill="white")


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Gera overlays (bbox + label) a partir de components_candidates.json"
    )
    parser.add_argument(
        "--candidates",
        type=str,
        default="data/components_output/components_candidates.json",
        help="JSON com candidatos rotulados (label/text/bbox)",
    )
    parser.add_argument(
        "--images-root",
        type=str,
        default="data/dataset_imagens",
        help="Pasta raiz onde estão as imagens (ex: data/dataset_imagens)",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="outputs/boxs_overlays",
        help="Pasta onde salvar os overlays gerados",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=22,
        help="Tamanho da fonte do label",
    )
    args = parser.parse_args()

    candidates_path = Path(args.candidates)
    images_root = Path(args.images_root)
    out_dir = Path(args.out_dir)

    if not candidates_path.exists():
        raise FileNotFoundError(f"Não achei candidates JSON: {candidates_path.resolve()}")

    ensure_dir(out_dir)

    data = json.loads(candidates_path.read_text(encoding="utf-8"))
    font = load_font(args.font_size)

    processed = 0
    missing = 0
    empty = 0

    for img_key, items in data.items():
        img_path = resolve_image_path(img_key, images_root)

        if not img_path.exists():
            print(f"[FALTOU] {img_key} -> tentei: {img_path.as_posix()}")
            missing += 1
            continue

        if not items:
            # imagem existe mas não teve nenhum candidato detectado
            empty += 1

        img = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        w, h = img.size

        # espessura proporcional ao tamanho da imagem
        line_w = max(3, int(min(w, h) * 0.003))  # ~0.3%

        for obj in items:
            label = obj.get("label", "unknown")
            bbox = obj.get("bbox")
            if not bbox or len(bbox) != 4:
                continue

            x1, y1, x2, y2 = bbox
            x1 = clamp(int(x1), 0, w - 1)
            y1 = clamp(int(y1), 0, h - 1)
            x2 = clamp(int(x2), 0, w - 1)
            y2 = clamp(int(y2), 0, h - 1)

            # bbox bem visível
            draw.rectangle([x1, y1, x2, y2], outline="red", width=line_w)

            # label curto (só a classe)
            draw_label(draw, x1, y1, f"{label}", font)

        out_path = out_dir / img_path.name
        img.save(out_path)
        processed += 1
        print(f"OK: {img_path.name} -> {out_path.as_posix()}")

    print("\nResumo:")
    print("Imagens com overlay gerado:", processed)
    print("Imagens faltando (não encontrei no disco):", missing)
    print("Imagens sem candidatos (items vazio):", empty)
    print("Saída:", out_dir.resolve())


if __name__ == "__main__":
    main()