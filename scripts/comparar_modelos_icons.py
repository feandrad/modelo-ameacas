"""
Script para comparar a eficiência de dois modelos de detecção de ícones
Compara Azure Custom Vision vs YOLO local
"""
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
import time

# ---------------------------
# Métricas de Comparação
# ---------------------------
def calculate_iou(box1: Dict, box2: Dict) -> float:
    """
    Calcula Intersection over Union (IoU) entre dois bounding boxes normalizados
    """
    # Converter de (left, top, width, height) para (x1, y1, x2, y2)
    x1_1 = box1["left"]
    y1_1 = box1["top"]
    x2_1 = box1["left"] + box1["width"]
    y2_1 = box1["top"] + box1["height"]
    
    x1_2 = box2["left"]
    y1_2 = box2["top"]
    x2_2 = box2["left"] + box2["width"]
    y2_2 = box2["top"] + box2["height"]
    
    # Calcular interseção
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i < x1_i or y2_i < y1_i:
        return 0.0
    
    intersection = (x2_i - x1_i) * (y2_i - y1_i)
    
    # Calcular união
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    union = area1 + area2 - intersection
    
    return intersection / union if union > 0 else 0.0


def normalize_label(label: str) -> str:
    """
    Normaliza labels para comparação (remove espaços, underscores, converte para maiúsculas)
    """
    return label.upper().replace("_", " ").replace("-", " ").strip()


def match_detections(dets1: List[Dict], dets2: List[Dict], iou_threshold: float = 0.5) -> Dict[str, Any]:
    """
    Encontra correspondências entre detecções de dois modelos
    Retorna estatísticas de matching
    """
    matched = []
    unmatched_1 = []
    unmatched_2 = list(range(len(dets2)))
    
    for i, det1 in enumerate(dets1):
        best_match = None
        best_iou = 0.0
        best_idx = -1
        
        for j in unmatched_2:
            det2 = dets2[j]
            
            # Verificar se as labels são compatíveis
            if normalize_label(det1["label"]) != normalize_label(det2["label"]):
                continue
            
            iou = calculate_iou(det1["bbox_norm"], det2["bbox_norm"])
            
            if iou > best_iou and iou >= iou_threshold:
                best_iou = iou
                best_match = det2
                best_idx = j
        
        if best_match:
            matched.append({
                "det1": det1,
                "det2": best_match,
                "iou": best_iou
            })
            unmatched_2.remove(best_idx)
        else:
            unmatched_1.append(det1)
    
    unmatched_2_dets = [dets2[i] for i in unmatched_2]
    
    return {
        "matched": matched,
        "unmatched_model1": unmatched_1,
        "unmatched_model2": unmatched_2_dets,
        "total_model1": len(dets1),
        "total_model2": len(dets2),
        "matched_count": len(matched)
    }


def calculate_metrics(match_results: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcula métricas de comparação
    """
    matched = match_results["matched_count"]
    total1 = match_results["total_model1"]
    total2 = match_results["total_model2"]
    
    # Precision: quantos do modelo 1 foram confirmados pelo modelo 2
    precision = matched / total1 if total1 > 0 else 0.0
    
    # Recall: quantos do modelo 2 foram detectados pelo modelo 1
    recall = matched / total2 if total2 > 0 else 0.0
    
    # F1-Score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Confiança média das detecções matched
    avg_conf1 = sum(m["det1"]["prob"] for m in match_results["matched"]) / matched if matched > 0 else 0.0
    avg_conf2 = sum(m["det2"]["prob"] for m in match_results["matched"]) / matched if matched > 0 else 0.0
    
    # IoU médio das detecções matched
    avg_iou = sum(m["iou"] for m in match_results["matched"]) / matched if matched > 0 else 0.0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "avg_confidence_model1": avg_conf1,
        "avg_confidence_model2": avg_conf2,
        "avg_iou": avg_iou
    }


# ---------------------------
# Análise por Classe
# ---------------------------
def analyze_by_class(all_matches: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Agrupa estatísticas por classe de componente
    """
    by_class = defaultdict(lambda: {
        "matched": 0,
        "unmatched_model1": 0,
        "unmatched_model2": 0,
        "total_iou": 0.0,
        "total_conf1": 0.0,
        "total_conf2": 0.0
    })
    
    for img, match_result in all_matches.items():
        for m in match_result["matched"]:
            label = normalize_label(m["det1"]["label"])
            by_class[label]["matched"] += 1
            by_class[label]["total_iou"] += m["iou"]
            by_class[label]["total_conf1"] += m["det1"]["prob"]
            by_class[label]["total_conf2"] += m["det2"]["prob"]
        
        for det in match_result["unmatched_model1"]:
            label = normalize_label(det["label"])
            by_class[label]["unmatched_model1"] += 1
        
        for det in match_result["unmatched_model2"]:
            label = normalize_label(det["label"])
            by_class[label]["unmatched_model2"] += 1
    
    # Calcular médias
    class_stats = {}
    for label, stats in by_class.items():
        matched = stats["matched"]
        class_stats[label] = {
            "matched": matched,
            "unmatched_model1": stats["unmatched_model1"],
            "unmatched_model2": stats["unmatched_model2"],
            "avg_iou": stats["total_iou"] / matched if matched > 0 else 0.0,
            "avg_conf_model1": stats["total_conf1"] / matched if matched > 0 else 0.0,
            "avg_conf_model2": stats["total_conf2"] / matched if matched > 0 else 0.0
        }
    
    return class_stats


# ---------------------------
# Relatório
# ---------------------------
def generate_report(comparison_results: Dict, class_stats: Dict, model1_name: str, model2_name: str) -> str:
    """
    Gera relatório em Markdown comparando os dois modelos
    """
    md = []
    md.append(f"# Comparação de Modelos de Detecção de Ícones")
    md.append("")
    md.append(f"**Modelo 1**: {model1_name}")
    md.append(f"**Modelo 2**: {model2_name}")
    md.append("")
    
    # Métricas globais
    md.append("## Métricas Globais")
    md.append("")
    
    total_matched = sum(r["matched_count"] for r in comparison_results.values())
    total_model1 = sum(r["total_model1"] for r in comparison_results.values())
    total_model2 = sum(r["total_model2"] for r in comparison_results.values())
    
    global_precision = total_matched / total_model1 if total_model1 > 0 else 0.0
    global_recall = total_matched / total_model2 if total_model2 > 0 else 0.0
    global_f1 = 2 * (global_precision * global_recall) / (global_precision + global_recall) if (global_precision + global_recall) > 0 else 0.0
    
    md.append(f"- **Total de detecções Modelo 1**: {total_model1}")
    md.append(f"- **Total de detecções Modelo 2**: {total_model2}")
    md.append(f"- **Detecções matched**: {total_matched}")
    md.append(f"- **Precision**: {global_precision:.2%}")
    md.append(f"- **Recall**: {global_recall:.2%}")
    md.append(f"- **F1-Score**: {global_f1:.2%}")
    md.append("")
    
    # Métricas por imagem
    md.append("## Métricas por Imagem")
    md.append("")
    md.append("| Imagem | Dets M1 | Dets M2 | Matched | Precision | Recall | F1 | Avg IoU |")
    md.append("|--------|---------|---------|---------|-----------|--------|-----|---------|")
    
    for img, match_result in comparison_results.items():
        metrics = calculate_metrics(match_result)
        img_name = Path(img).name
        md.append(
            f"| {img_name} | {match_result['total_model1']} | {match_result['total_model2']} | "
            f"{match_result['matched_count']} | {metrics['precision']:.2%} | {metrics['recall']:.2%} | "
            f"{metrics['f1_score']:.2%} | {metrics['avg_iou']:.3f} |"
        )
    
    md.append("")
    
    # Análise por classe
    md.append("## Análise por Classe de Componente")
    md.append("")
    md.append("| Classe | Matched | Não-M1 | Não-M2 | Avg IoU | Conf M1 | Conf M2 |")
    md.append("|--------|---------|--------|--------|---------|---------|---------|")
    
    for label in sorted(class_stats.keys()):
        stats = class_stats[label]
        md.append(
            f"| {label} | {stats['matched']} | {stats['unmatched_model1']} | "
            f"{stats['unmatched_model2']} | {stats['avg_iou']:.3f} | "
            f"{stats['avg_conf_model1']:.2%} | {stats['avg_conf_model2']:.2%} |"
        )
    
    md.append("")
    
    # Conclusões
    md.append("## Conclusões")
    md.append("")
    
    if global_f1 > 0.8:
        md.append("✅ **Alta concordância** entre os modelos (F1 > 80%)")
    elif global_f1 > 0.6:
        md.append("⚠️ **Concordância moderada** entre os modelos (F1 60-80%)")
    else:
        md.append("❌ **Baixa concordância** entre os modelos (F1 < 60%)")
    
    md.append("")
    
    # Identificar melhor modelo por classe
    md.append("### Melhor Modelo por Classe")
    md.append("")
    
    for label in sorted(class_stats.keys()):
        stats = class_stats[label]
        if stats["avg_conf_model1"] > stats["avg_conf_model2"]:
            md.append(f"- **{label}**: Modelo 1 (confiança {stats['avg_conf_model1']:.2%} vs {stats['avg_conf_model2']:.2%})")
        elif stats["avg_conf_model2"] > stats["avg_conf_model1"]:
            md.append(f"- **{label}**: Modelo 2 (confiança {stats['avg_conf_model2']:.2%} vs {stats['avg_conf_model1']:.2%})")
        else:
            md.append(f"- **{label}**: Empate")
    
    md.append("")
    
    return "\n".join(md)


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Compara eficiência de dois modelos de detecção de ícones"
    )
    parser.add_argument(
        "--model1",
        type=str,
        default="data/predictions/predictions.json",
        help="JSON com predições do Modelo 1 (Azure Custom Vision)"
    )
    parser.add_argument(
        "--model2",
        type=str,
        default="data/predictions/predictions_yolo.json",
        help="JSON com predições do Modelo 2 (YOLO local)"
    )
    parser.add_argument(
        "--model1-name",
        type=str,
        default="Azure Custom Vision",
        help="Nome do Modelo 1 para o relatório"
    )
    parser.add_argument(
        "--model2-name",
        type=str,
        default="YOLO Local",
        help="Nome do Modelo 2 para o relatório"
    )
    parser.add_argument(
        "--out-report",
        type=str,
        default="outputs/reports/comparacao_modelos.md",
        help="Arquivo de saída do relatório (Markdown)"
    )
    parser.add_argument(
        "--out-json",
        type=str,
        default="outputs/reports/comparacao_modelos.json",
        help="Arquivo de saída dos dados (JSON)"
    )
    parser.add_argument(
        "--iou-threshold",
        type=float,
        default=0.5,
        help="Threshold de IoU para considerar match (0-1)"
    )
    
    args = parser.parse_args()
    
    # Carregar predições
    model1_path = Path(args.model1)
    model2_path = Path(args.model2)
    
    if not model1_path.exists():
        raise FileNotFoundError(f"Predições do Modelo 1 não encontradas: {model1_path}")
    
    if not model2_path.exists():
        raise FileNotFoundError(f"Predições do Modelo 2 não encontradas: {model2_path}")
    
    print(f"Carregando predições...")
    print(f"Modelo 1: {model1_path}")
    print(f"Modelo 2: {model2_path}")
    
    model1_data = json.loads(model1_path.read_text(encoding="utf-8"))
    model2_data = json.loads(model2_path.read_text(encoding="utf-8"))
    
    # Extrair items (suporta formato com/sem meta)
    model1_items = model1_data.get("items", model1_data)
    model2_items = model2_data.get("items", model2_data)
    
    # Encontrar imagens em comum
    common_images = set(model1_items.keys()) & set(model2_items.keys())
    
    if not common_images:
        raise ValueError("Nenhuma imagem em comum entre os dois modelos!")
    
    print(f"\nImagens em comum: {len(common_images)}")
    print(f"IoU threshold: {args.iou_threshold}")
    print("\nComparando detecções...\n")
    
    # Comparar cada imagem
    comparison_results = {}
    
    for img in sorted(common_images):
        dets1 = model1_items[img]
        dets2 = model2_items[img]
        
        match_result = match_detections(dets1, dets2, args.iou_threshold)
        comparison_results[img] = match_result
        
        metrics = calculate_metrics(match_result)
        print(f"{Path(img).name}: M1={len(dets1)} M2={len(dets2)} Matched={match_result['matched_count']} F1={metrics['f1_score']:.2%}")
    
    # Análise por classe
    class_stats = analyze_by_class(comparison_results)
    
    # Gerar relatório
    report = generate_report(comparison_results, class_stats, args.model1_name, args.model2_name)
    
    # Salvar relatório
    out_report = Path(args.out_report)
    out_json = Path(args.out_json)
    
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    
    out_report.write_text(report, encoding="utf-8")
    
    # Salvar dados JSON
    output_data = {
        "meta": {
            "model1_name": args.model1_name,
            "model2_name": args.model2_name,
            "iou_threshold": args.iou_threshold,
            "images_compared": len(common_images)
        },
        "comparison_results": comparison_results,
        "class_stats": class_stats
    }
    
    out_json.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print("\n=== RESUMO ===")
    print(f"Relatório salvo em: {out_report}")
    print(f"Dados JSON salvos em: {out_json}")
    print(f"\nImagens comparadas: {len(common_images)}")


if __name__ == "__main__":
    main()
