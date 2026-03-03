import json
import re
import argparse
from pathlib import Path

# -----------------------------------------
# Regras (expanda à vontade)
# -----------------------------------------
LABEL_RULES = {
    "user": [r"\buser\b", r"\busu[aá]rios?\b", r"\bclient\b", r"\bconsumer\b"],
    "api_gateway": [r"\bapi\s*gateway\b", r"\bgateway\b", r"\bapi\s*management\b", r"\bapim\b"],
    "load_balancer": [r"\bload\s*balancer\b", r"\balb\b", r"\belb\b", r"\blb\b"],
    "network": [r"\bvpc\b", r"\bvnet\b", r"\bvirtual\s+private\s+cloud\b", r"\bsubnet\b", r"\bpublic\s*subnet\b", r"\bprivate\s*subnet\b", r"\bavailability\s*zone\b", r"\baz\b"],
    "app_service": [r"\bserver\b", r"\bec2\b", r"\bapi\s*server\b", r"\bapp\s*server\b", r"\bauto\s*scaling\b", r"\basg\b", r"\bsei\b", r"\bsip\b", r"\bsolr\b", r"\bapplication\b"],
    "database": [r"\bdatabase\b", r"\bdb\b", r"\brds\b", r"\bpostgres\b", r"\bmysql\b", r"\bsql\b"],
    "cache": [r"\bcache\b", r"\belasticache\b", r"\bredis\b", r"\bmemcached\b"],
    "storage": [r"\bstorage\b", r"\bs3\b", r"\befs\b", r"\bnfs\b", r"\bfile\s*system\b"],
    "observability": [r"\bmonitoring\b", r"\bcloudwatch\b", r"\blogs?\b", r"\bobservability\b"],
    "security": [r"\bsecurity\b", r"\bwaf\b", r"\bshield\b", r"\biam\b", r"\bentra\b", r"\bcognito\b", r"\bauth(entication|orization)?\b", r"\blogin\b", r"\bss[oa]\b", r"\bcloudtrail\b", r"\bkms\b", r"\bkey\s*management\b"],
    "backup_dr": [r"\bbackup\b", r"\bdr\b", r"\bdisaster\s*recovery\b"],
    "external_service": [r"\bsaas\b", r"\brest\b", r"\bsoap\b", r"\bweb\s*services?\b", r"\bbackend\b"],
}


# -----------------------------------------
# Helpers
# -----------------------------------------
def normalize_text(t: str) -> str:
    t = (t or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def match_label(text_norm: str):
    for label, patterns in LABEL_RULES.items():
        for pat in patterns:
            if re.search(pat, text_norm, flags=re.IGNORECASE):
                return label
    return None


def poly_to_xyxy(poly):
    """
    poly: [{"x":..., "y":...}, ...]
    retorna [x1,y1,x2,y2]
    """
    xs = [p.get("x") for p in (poly or []) if p and p.get("x") is not None]
    ys = [p.get("y") for p in (poly or []) if p and p.get("y") is not None]
    if not xs or not ys:
        return None
    return [min(xs), min(ys), max(xs), max(ys)]


def merge_boxes(a, b):
    return [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]


def x_overlap_ratio(a, b):
    # overlap / menor largura
    left = max(a[0], b[0])
    right = min(a[2], b[2])
    overlap = max(0, right - left)
    wa = max(1, a[2] - a[0])
    wb = max(1, b[2] - b[0])
    return overlap / min(wa, wb)


def group_lines(lines, y_gap=35, min_x_overlap=0.25):
    """
    Junta linhas que estão na mesma 'coluna' (sobreposição X)
    e com pequeno gap vertical.
    """
    items = []
    for ln in (lines or []):
        box = poly_to_xyxy(ln.get("bbox", []))
        if not box:
            continue
        items.append({"text": ln.get("text", ""), "box": box})

    # ordena por topo (y1) e depois x1
    items.sort(key=lambda x: (x["box"][1], x["box"][0]))

    groups = []
    for it in items:
        placed = False
        for g in groups:
            last = g["box"]
            same_col = x_overlap_ratio(last, it["box"]) >= min_x_overlap
            close_y = (it["box"][1] - last[3]) <= y_gap  # gap entre o fim do último e topo do novo
            if same_col and close_y:
                g["text"] += " " + it["text"]
                g["box"] = merge_boxes(g["box"], it["box"])
                placed = True
                break
        if not placed:
            groups.append({"text": it["text"], "box": it["box"]})

    return groups


# -----------------------------------------
# Leitura do OCR (novo + antigo)
# -----------------------------------------
def load_ocr_as_map(ocr_path: Path) -> dict:
    """
    Retorna sempre um dict no formato:
      { "img_path": [ {text, bbox}, ... ] }

    Suporta:
    - FORMATO NOVO: {"meta":..., "items": {"img": {"status":..., "lines":[...]}}}
    - FORMATO ANTIGO: {"img": [ {text,bbox}, ... ]}
    """
    raw = json.loads(ocr_path.read_text(encoding="utf-8"))

    # Novo formato
    if isinstance(raw, dict) and "items" in raw and isinstance(raw["items"], dict):
        out = {}
        for img_path, payload in raw["items"].items():
            if isinstance(payload, dict) and payload.get("status") == "ok":
                out[img_path] = payload.get("lines", []) or []
            else:
                # se erro, mantém lista vazia pra rastreabilidade
                out[img_path] = []
        return out

    # Antigo formato
    if isinstance(raw, dict):
        # supõe que seja {img_path: [linhas]}
        return raw

    raise ValueError("OCR JSON em formato desconhecido. Esperado dict.")


def main():
    parser = argparse.ArgumentParser(description="Gera candidates/review a partir do OCR JSON.")
    parser.add_argument("--ocr", type=str, default="data/ocr/ocr_result.json", help="Entrada OCR JSON")
    parser.add_argument("--out-cand", type=str, default="data/components_output/components_candidates.json", help="Saída candidates")
    parser.add_argument("--out-review", type=str, default="data/components_output/components_review.json", help="Saída review")
    parser.add_argument("--y-gap", type=int, default=40, help="Gap vertical máximo para merge")
    parser.add_argument("--min-x-overlap", type=float, default=0.20, help="Sobreposição X mínima para merge")
    parser.add_argument("--min-review-len", type=int, default=8, help="Tamanho mínimo (normalizado) pra entrar no review")
    parser.add_argument("--review-limit", type=int, default=30, help="Limite de itens no review por imagem")
    args = parser.parse_args()

    ocr_path = Path(args.ocr)
    out_cand_path = Path(args.out_cand)
    out_review_path = Path(args.out_review)

    if not ocr_path.exists():
        raise FileNotFoundError(f"Não achei {ocr_path.resolve()}")

    data = load_ocr_as_map(ocr_path)

    out_cand = {}
    out_review = {}

    total_imgs = 0
    total_lines = 0
    total_groups = 0
    total_matched = 0

    for img_path, lines in data.items():
        total_imgs += 1
        total_lines += len(lines)

        groups = group_lines(lines, y_gap=args.y_gap, min_x_overlap=args.min_x_overlap)
        total_groups += len(groups)

        candidates = []
        review = []

        for g in groups:
            text = g["text"]
            box = g["box"]
            text_norm = normalize_text(text)
            label = match_label(text_norm)

            if label:
                candidates.append({"label": label, "text": text, "bbox": box})
                total_matched += 1
            else:
                if len(text_norm) >= args.min_review_len:
                    review.append({"text": text, "bbox": box})

        # limita review por imagem (ordena por texto mais longo primeiro)
        review = sorted(review, key=lambda x: len(normalize_text(x["text"])), reverse=True)[: args.review_limit]

        out_cand[img_path] = candidates
        out_review[img_path] = review

    out_cand_path.parent.mkdir(parents=True, exist_ok=True)
    out_review_path.parent.mkdir(parents=True, exist_ok=True)

    out_cand_path.write_text(json.dumps(out_cand, ensure_ascii=False, indent=2), encoding="utf-8")
    out_review_path.write_text(json.dumps(out_review, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== STATS ===")
    print("imagens:", total_imgs)
    print("linhas OCR:", total_lines)
    print("grupos após merge:", total_groups)
    print("matches (com label):", total_matched)
    print("salvo candidates:", out_cand_path.as_posix())
    print("salvo review:", out_review_path.as_posix())


if __name__ == "__main__":
    main()