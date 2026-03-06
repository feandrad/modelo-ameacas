"""
Script para detecção de setas/conexões usando modelo YOLO local (best_arrows.pt)
Detecta as ligações entre componentes no diagrama de arquitetura
"""
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple

try:
    from ultralytics import YOLO
    import torch
except ImportError:
    print("ERRO: ultralytics não instalado. Execute: pip install ultralytics")
    exit(1)

from PIL import Image

# ---------------------------
# Constantes
# ---------------------------
EXTS = {".png", ".jpg", ".jpeg", ".webp"}


# ---------------------------
# IO helpers
# ---------------------------
def list_images(input_dir: Path, recursive: bool = True) -> List[Path]:
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
# Análise de Conexões
# ---------------------------
def calculate_arrow_endpoints(arrow: Dict[str, Any]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Calcula os pontos inicial e final da seta
    
    Prioridade:
    1. Usa keypoints se disponíveis (amarelo=início, vermelho=ponta)
    2. Fallback: estima pelos cantos do bbox
    
    Retorna: ((x_start, y_start), (x_end, y_end))
    """
    img_width = arrow["img_width"]
    img_height = arrow["img_height"]
    
    # Se tem keypoints, usa eles (mais preciso!)
    if "keypoints" in arrow:
        kpts = arrow["keypoints"]
        start_x = int(kpts["start"]["x"] * img_width)
        start_y = int(kpts["start"]["y"] * img_height)
        end_x = int(kpts["end"]["x"] * img_width)
        end_y = int(kpts["end"]["y"] * img_height)
        return ((start_x, start_y), (end_x, end_y))
    
    # Fallback: estima pelo bbox (menos preciso)
    bbox = arrow["bbox_norm"]
    left = bbox["left"]
    top = bbox["top"]
    width = bbox["width"]
    height = bbox["height"]
    
    center_x = int((left + width / 2) * img_width)
    center_y = int((top + height / 2) * img_height)
    
    # Se a seta é mais horizontal
    if width > height:
        x1 = int(left * img_width)
        x2 = int((left + width) * img_width)
        y1 = y2 = center_y
    else:  # Mais vertical
        x1 = x2 = center_x
        y1 = int(top * img_height)
        y2 = int((top + height) * img_height)
    
    return ((x1, y1), (x2, y2))


def find_connected_components(arrow_endpoints: Tuple[Tuple[int, int], Tuple[int, int]], 
                              components: List[Dict[str, Any]],
                              img_width: int,
                              img_height: int,
                              tolerance: int = 50) -> Tuple[Dict, Dict]:
    """
    Encontra quais componentes estão conectados pela seta
    Retorna: (source_component, target_component)
    """
    (x1, y1), (x2, y2) = arrow_endpoints
    
    source = None
    target = None
    min_dist_source = float('inf')
    min_dist_target = float('inf')
    
    for comp in components:
        bbox = comp["bbox_norm"]
        
        # Centro do componente
        comp_center_x = int((bbox["left"] + bbox["width"] / 2) * img_width)
        comp_center_y = int((bbox["top"] + bbox["height"] / 2) * img_height)
        
        # Distância do início da seta ao componente
        dist_start = ((x1 - comp_center_x) ** 2 + (y1 - comp_center_y) ** 2) ** 0.5
        
        # Distância do fim da seta ao componente
        dist_end = ((x2 - comp_center_x) ** 2 + (y2 - comp_center_y) ** 2) ** 0.5
        
        # Componente mais próximo do início é a origem
        if dist_start < min_dist_source and dist_start < tolerance:
            min_dist_source = dist_start
            source = comp
        
        # Componente mais próximo do fim é o destino
        if dist_end < min_dist_target and dist_end < tolerance:
            min_dist_target = dist_end
            target = comp
    
    return source, target


# ---------------------------
# YOLO Prediction
# ---------------------------
def run_yolo_prediction(model: YOLO, img_path: Path, threshold: float) -> List[Dict[str, Any]]:
    """
    Executa predição YOLO para setas
    Extrai keypoints se disponíveis (amarelo=início, vermelho=ponta)
    """
    results = model.predict(source=str(img_path), conf=threshold, verbose=False)
    
    detections = []
    
    for result in results:
        boxes = result.boxes
        img_width = result.orig_shape[1]
        img_height = result.orig_shape[0]
        
        # Verificar se tem keypoints
        has_keypoints = hasattr(result, 'keypoints') and result.keypoints is not None
        
        for idx, box in enumerate(boxes):
            # Coordenadas xyxy (x1, y1, x2, y2)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            # Normalizar para 0-1
            left = float(x1 / img_width)
            top = float(y1 / img_height)
            width = float((x2 - x1) / img_width)
            height = float((y2 - y1) / img_height)
            
            # Classe e confiança
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            
            detection = {
                "label": label,
                "prob": conf,
                "bbox_norm": {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height
                },
                "img_width": img_width,
                "img_height": img_height
            }
            
            # Extrair keypoints se disponíveis
            if has_keypoints and len(result.keypoints.xy) > idx:
                kpts = result.keypoints.xy[idx].cpu().numpy()
                if len(kpts) >= 2:
                    # kpts[0] = início (amarelo), kpts[1] = ponta (vermelho)
                    detection["keypoints"] = {
                        "start": {
                            "x": float(kpts[0][0] / img_width),
                            "y": float(kpts[0][1] / img_height)
                        },
                        "end": {
                            "x": float(kpts[1][0] / img_width),
                            "y": float(kpts[1][1] / img_height)
                        }
                    }
            
            detections.append(detection)
    
    return detections


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Detecção de setas/conexões usando modelo YOLO local (best_arrows.pt)"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="models/best_arrows.pt",
        help="Caminho para o modelo YOLO de setas (.pt)"
    )
    parser.add_argument(
        "--input", 
        type=str, 
        default="imagens_validacao",
        help="Pasta com imagens para prever"
    )
    parser.add_argument(
        "--components",
        type=str,
        default="data/predictions/predictions_yolo.json",
        help="JSON com componentes detectados (para mapear conexões)"
    )
    parser.add_argument(
        "--out", 
        type=str, 
        default="data/arrows_output/arrows_detected.json",
        help="JSON de saída com setas detectadas"
    )
    parser.add_argument(
        "--out-connections",
        type=str,
        default="data/arrows_output/connections.json",
        help="JSON de saída com conexões mapeadas"
    )
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.3,
        help="Confiança mínima (0-1)"
    )
    parser.add_argument(
        "--no-recursive", 
        action="store_true",
        help="Não buscar imagens em subpastas"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=0,
        help="Limita quantas imagens processar (0 = todas)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device para inferência: 'cpu', 'cuda', 'mps' (Mac M1/M2)"
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=50,
        help="Tolerância em pixels para conectar seta a componente"
    )
    parser.add_argument(
        "--invert-direction",
        action="store_true",
        help="Inverte direção das setas (útil se detecção estiver ao contrário)"
    )
    
    args = parser.parse_args()

    # Validar modelo
    model_path = Path(args.model)
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path.resolve()}")

    # Carregar componentes (se disponível)
    components_data = {}
    components_path = Path(args.components)
    if components_path.exists():
        print(f"Carregando componentes de: {components_path}")
        comp_json = json.loads(components_path.read_text(encoding="utf-8"))
        components_data = comp_json.get("items", comp_json)
    else:
        print(f"AVISO: Arquivo de componentes não encontrado: {components_path}")
        print("Continuando sem mapeamento de conexões...")

    # Carregar modelo YOLO
    print(f"Carregando modelo de setas: {model_path}")
    print(f"Device: {args.device}")
    
    model = YOLO(str(model_path))
    
    # Verificar device disponível
    if args.device == "mps" and not torch.backends.mps.is_available():
        print("AVISO: MPS não disponível, usando CPU")
        args.device = "cpu"
    elif args.device == "cuda" and not torch.cuda.is_available():
        print("AVISO: CUDA não disponível, usando CPU")
        args.device = "cpu"
    
    # Listar imagens
    input_dir = Path(args.input)
    out_file = Path(args.out)
    out_connections = Path(args.out_connections)
    ensure_dir(out_file.parent)

    images = list_images(input_dir, recursive=not args.no_recursive)
    if args.limit and args.limit > 0:
        images = images[:args.limit]

    print(f"\nProcessando {len(images)} imagens...")
    print(f"Threshold: {args.threshold}")
    print(f"Classes disponíveis: {model.names}\n")

    arrows_results = {}
    connections_results = {}
    failed = 0
    total_arrows = 0
    total_connections = 0

    for i, img_path in enumerate(images, start=1):
        try:
            # Detectar setas
            arrows = run_yolo_prediction(
                model=model,
                img_path=img_path,
                threshold=args.threshold
            )

            arrows_results[img_path.as_posix()] = arrows
            total_arrows += len(arrows)
            
            # Mapear conexões se temos componentes
            img_key = img_path.as_posix()
            if img_key in components_data and arrows:
                components = components_data[img_key]
                connections = []
                
                for arrow in arrows:
                    endpoints = calculate_arrow_endpoints(arrow)
                    
                    source, target = find_connected_components(
                        endpoints,
                        components,
                        arrow["img_width"],
                        arrow["img_height"],
                        args.tolerance
                    )
                    
                    if source and target:
                        connections.append({
                            "from": source["label"],
                            "to": target["label"],
                            "arrow_type": arrow["label"],
                            "confidence": arrow["prob"]
                        })
                        total_connections += 1
                
                connections_results[img_key] = connections
            
            print(f"[{i}/{len(images)}] OK   - {img_path.name} | setas: {len(arrows)}")

        except Exception as e:
            failed += 1
            arrows_results[img_path.as_posix()] = []
            print(f"[{i}/{len(images)}] ERRO - {img_path.name}: {e}")

    # Salvar resultados de setas
    arrows_payload = {
        "meta": {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "model_path": model_path.as_posix(),
            "model_type": "YOLO",
            "device": args.device,
            "input_dir": input_dir.as_posix(),
            "images_total": len(images),
            "failed": failed,
            "threshold": args.threshold,
            "arrows_total": total_arrows,
            "classes": model.names,
        },
        "items": arrows_results,
    }

    out_file.write_text(
        json.dumps(arrows_payload, ensure_ascii=False, indent=2), 
        encoding="utf-8"
    )

    # Salvar conexões mapeadas
    if connections_results:
        connections_payload = {
            "meta": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "connections_total": total_connections,
                "tolerance_pixels": args.tolerance,
            },
            "items": connections_results,
        }
        
        out_connections.write_text(
            json.dumps(connections_payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    print("\n=== RESUMO ===")
    print("Modelo:", model_path.as_posix())
    print("Setas detectadas salvas em:", out_file.as_posix())
    if connections_results:
        print("Conexões mapeadas salvas em:", out_connections.as_posix())
    print("Imagens processadas:", len(images))
    print("Falhas:", failed)
    print("Setas detectadas:", total_arrows)
    print("Conexões mapeadas:", total_connections)


if __name__ == "__main__":
    main()
