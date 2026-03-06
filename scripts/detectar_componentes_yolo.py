"""
Script para detecção de componentes usando modelo YOLO local (best_icons.pt)
Substitui a chamada ao Azure Custom Vision por inferência local
"""
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

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
# YOLO Prediction
# ---------------------------
def run_yolo_prediction(model: YOLO, img_path: Path, threshold: float) -> List[Dict[str, Any]]:
    """
    Executa predição YOLO e retorna detecções no formato compatível com o sistema existente
    
    Retorna lista de dicts:
    {
        "label": str,
        "prob": float,
        "bbox_norm": {
            "left": float,
            "top": float,
            "width": float,
            "height": float
        }
    }
    """
    results = model.predict(source=str(img_path), conf=threshold, verbose=False)
    
    detections = []
    
    for result in results:
        boxes = result.boxes
        img_width = result.orig_shape[1]
        img_height = result.orig_shape[0]
        
        for box in boxes:
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
            
            detections.append({
                "label": label,
                "prob": conf,
                "bbox_norm": {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height
                }
            })
    
    return detections


# ---------------------------
# Main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Inferência usando modelo YOLO local (best_icons.pt)"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="models/best_icons.pt",
        help="Caminho para o modelo YOLO (.pt)"
    )
    parser.add_argument(
        "--input", 
        type=str, 
        default="imagens_validacao",
        help="Pasta com imagens para prever"
    )
    parser.add_argument(
        "--out", 
        type=str, 
        default="data/predictions/predictions_yolo.json",
        help="JSON de saída"
    )
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.5,
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
    
    args = parser.parse_args()

    # Validar modelo
    model_path = Path(args.model)
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path.resolve()}")

    # Carregar modelo YOLO
    print(f"Carregando modelo: {model_path}")
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
    ensure_dir(out_file.parent)

    images = list_images(input_dir, recursive=not args.no_recursive)
    if args.limit and args.limit > 0:
        images = images[:args.limit]

    print(f"\nProcessando {len(images)} imagens...")
    print(f"Threshold: {args.threshold}")
    print(f"Classes disponíveis: {model.names}\n")

    results = {}
    failed = 0
    total_kept = 0

    for i, img_path in enumerate(images, start=1):
        try:
            dets = run_yolo_prediction(
                model=model,
                img_path=img_path,
                threshold=args.threshold
            )

            results[img_path.as_posix()] = dets
            total_kept += len(dets)
            print(f"[{i}/{len(images)}] OK   - {img_path.name} | dets: {len(dets)}")

        except Exception as e:
            failed += 1
            results[img_path.as_posix()] = []
            print(f"[{i}/{len(images)}] ERRO - {img_path.name}: {e}")

    # Salvar resultados
    payload = {
        "meta": {
            "created_at": datetime.utcnow().isoformat() + "Z",
            "model_path": model_path.as_posix(),
            "model_type": "YOLO",
            "device": args.device,
            "input_dir": input_dir.as_posix(),
            "images_total": len(images),
            "failed": failed,
            "threshold": args.threshold,
            "detections_total": total_kept,
            "classes": model.names,
        },
        "items": results,
    }

    out_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), 
        encoding="utf-8"
    )

    print("\n=== RESUMO ===")
    print("Modelo:", model_path.as_posix())
    print("Salvo:", out_file.as_posix())
    print("Imagens processadas:", len(images))
    print("Falhas:", failed)
    print("Detecções totais:", total_kept)


if __name__ == "__main__":
    main()
