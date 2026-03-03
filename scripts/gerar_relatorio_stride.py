import json
import argparse
from pathlib import Path
from datetime import datetime

# ---------------------------
# Mapeamento Tag -> Tipo
# ---------------------------
TAG_TO_TYPE = {
    "SEGURANÇA": "security",
    "SECURITY": "security",
    "WAF": "security",

    "VPC": "network",
    "SUBNET_PRIVATE": "network",
    "SUBNET PRIVATE": "network",
    "SUBNET_PUBLIC": "network",
    "SUBNET PUBLIC": "network",

    "API_GATEWAY": "api",
    "API GATEWAY": "api",

    "LOAD_BALANCER": "lb",
    "LOAD BALANCER": "lb",

    "BANCO DE DADOS": "database",
    "DATABASE": "database",

    "ARMAZENAGEM": "storage",
    "STORAGE": "storage",

    "USUÁRIO": "user",
    "USER": "user",

    "MONITORING": "monitoring",
    "MONITORANDO": "monitoring",
}

# ---------------------------
# STRIDE por tipo
# ---------------------------
STRIDE_RULES = {
    "user": ["Spoofing", "Repudiation"],
    "api": ["Spoofing", "Tampering", "Denial of Service", "Elevation of Privilege"],
    "security": ["Tampering", "Information Disclosure", "Denial of Service"],
    "network": ["Information Disclosure", "Tampering"],
    "lb": ["Denial of Service", "Tampering"],
    "database": ["Tampering", "Information Disclosure", "Repudiation"],
    "storage": ["Information Disclosure", "Tampering"],
    "monitoring": ["Repudiation", "Information Disclosure"],
    "unknown": ["Information Disclosure"],
}

MITIGATIONS = {
    "Spoofing": ["MFA", "OAuth2/OIDC", "IAM least privilege", "mTLS quando aplicável"],
    "Tampering": ["TLS", "validação de entrada", "WAF rules", "assinatura/hash de integridade"],
    "Repudiation": ["logs e auditoria", "trilha imutável", "correlação de eventos"],
    "Information Disclosure": ["criptografia em trânsito e repouso", "segredos em vault", "segmentação de rede"],
    "Denial of Service": ["rate limit", "autoscaling", "WAF/Shield", "circuit breaker"],
    "Elevation of Privilege": ["least privilege", "RBAC/scopes", "hardening", "patching"],
}


def norm_tag(t: str) -> str:
    return (t or "").strip()


def load_predictions_any_format(path: Path) -> dict:
    """
    Suporta:
    - Formato novo: {"meta": {...}, "items": { "img": [preds...] }}
    - Formato antigo: { "img": [preds...] }
    Retorna sempre: { "img": [preds...] }
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "items" in raw and isinstance(raw["items"], dict):
        return raw["items"]
    if isinstance(raw, dict):
        return raw
    raise ValueError("predictions.json em formato desconhecido.")


def tag_to_type(tag: str) -> str:
    # tenta direto, depois upper
    if tag in TAG_TO_TYPE:
        return TAG_TO_TYPE[tag]
    up = tag.upper()
    return TAG_TO_TYPE.get(up, "unknown")


def build_threats_for_image(preds: list) -> list[dict]:
    threats = []
    for p in preds or []:
        tag = norm_tag(p.get("label", ""))
        prob = p.get("prob", None)

        comp_type = tag_to_type(tag)
        stride_list = STRIDE_RULES.get(comp_type, STRIDE_RULES["unknown"])

        for s in stride_list:
            threats.append({
                "component_tag": tag,
                "component_type": comp_type,
                "prob": prob,
                "stride": s,
                "mitigations": MITIGATIONS.get(s, []),
            })
    return threats


def threats_to_markdown(threats_by_img: dict, generated_at: str) -> str:
    md = []
    md.append("# Relatório de Modelagem de Ameaças (STRIDE) — MVP")
    md.append("")
    md.append(f"Gerado em: {generated_at}")
    md.append("")
    md.append("## Objetivo")
    md.append("Gerar automaticamente um relatório STRIDE a partir de um diagrama de arquitetura (imagem), detectando componentes com modelo supervisionado treinado no Azure Custom Vision.")
    md.append("")

    for img, threats in threats_by_img.items():
        md.append("---")
        md.append(f"## Diagrama: `{img}`")
        md.append("")

        if not threats:
            md.append("Nenhuma ameaça gerada (sem detecções acima do limiar).")
            md.append("")
            continue

        by_stride = {}
        for t in threats:
            by_stride.setdefault(t["stride"], []).append(t)

        for stride, items in by_stride.items():
            md.append(f"### {stride}")
            for t in items:
                md.append(f"- **Componente**: {t['component_tag']} (tipo: {t['component_type']}, prob: {t.get('prob')})")
                if t["mitigations"]:
                    md.append(f"  - **Contramedidas**: {', '.join(t['mitigations'])}")
            md.append("")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Gera threat_model.json e relatório STRIDE (.md) a partir de predictions.json")
    parser.add_argument("--pred", type=str, default="data/predictions/predictions.json", help="Entrada predictions.json")
    parser.add_argument("--out-md", type=str, default="outputs/reports/relatorio_final.md", help="Saída do relatório Markdown")
    parser.add_argument("--out-json", type=str, default="data/modelo_ameacas/threat_model.json", help="Saída JSON intermediária (opcional)")
    parser.add_argument("--skip-json", action="store_true", help="Não salvar o threat_model.json (só gerar o .md)")
    args = parser.parse_args()

    pred_path = Path(args.pred)
    out_md = Path(args.out_md)
    out_json = Path(args.out_json)

    if not pred_path.exists():
        raise FileNotFoundError(f"Não achei: {pred_path.resolve()}")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    preds_by_img = load_predictions_any_format(pred_path)

    threats_by_img = {}
    for img, preds in preds_by_img.items():
        threats_by_img[img] = build_threats_for_image(preds)

    # salva JSON (se quiser)
    if not args.skip_json:
        out_json.write_text(json.dumps(threats_by_img, ensure_ascii=False, indent=2), encoding="utf-8")
        print("OK -> threat_model:", out_json.as_posix())

    # gera markdown
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_text = threats_to_markdown(threats_by_img, generated_at)
    out_md.write_text(md_text, encoding="utf-8")
    print("OK -> relatório:", out_md.as_posix())


if __name__ == "__main__":
    main()