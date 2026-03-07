"""
Script para visualizar detecções dos modelos YOLO
Desenha boxes e arrows nas imagens originais
"""
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import cv2
import numpy as np

# Cores para diferentes tipos de detecções (BGR)
COLORS = {
    "component": (0, 255, 0),      # Verde para componentes
    "arrow": (255, 0, 0),          # Azul para setas
    "keypoint_start": (0, 255, 255),  # Amarelo para início da seta
    "keypoint_end": (0, 0, 255),      # Vermelho para ponta da seta
}

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def draw_bbox(img: np.ndarray, bbox_norm: Dict, label: str, prob: float, color: tuple):
    """Desenha bounding box na imagem"""
    h, w = img.shape[:2]
    
    left = int(bbox_norm["left"] * w)
    top = int(bbox_norm["top"] * h)
    width = int(bbox_norm["width"] * w)
    height = int(bbox_norm["height"] * h)
    
    # Desenhar retângulo
    cv2.rectangle(img, (left, top), (left + width, top + height), color, 2)
    
    # Preparar texto
    text = f"{label}: {prob:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    
    # Calcular tamanho do texto para background
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Desenhar background do texto
    cv2.rectangle(img, (left, top - text_h - 5), (left + text_w, top), color, -1)
    
    # Desenhar texto
    cv2.putText(img, text, (left, top - 5), font, font_scale, (255, 255, 255), thickness)

def draw_keypoints(img: np.ndarray, keypoints: Dict):
    """Desenha keypoints da seta (início e fim)"""
    h, w = img.shape[:2]
    
    # Início (amarelo)
    start_x = int(keypoints["start"]["x"] * w)
    start_y = int(keypoints["start"]["y"] * h)
    cv2.circle(img, (start_x, start_y), 5, COLORS["keypoint_start"], -1)
    
    # Fim (vermelho)
    end_x = int(keypoints["end"]["x"] * w)
    end_y = int(keypoints["end"]["y"] * h)
    cv2.circle(img, (end_x, end_y), 5, COLORS["keypoint_end"], -1)
    
    # Linha conectando
    cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 0), 2)

def visualize_detections(
    img_path: Path,
    components: List[Dict[str, Any]],
    arrows: List[Dict[str, Any]],
    output_path: Path
):
    """Visualiza todas as detecções em uma imagem"""
    # Carregar imagem
    img = cv2.imread(str(img_path))
    if img is None:
        raise ValueError(f"Não foi possível carregar imagem: {img_path}")
    
    # Desenhar componentes
    for comp in components:
        draw_bbox(img, comp["bbox_norm"], comp["label"], comp["prob"], COLORS["component"])
    
    # Desenhar setas
    for arrow in arrows:
        draw_bbox(img, arrow["bbox_norm"], arrow["label"], arrow["prob"], COLORS["arrow"])
        
        # Desenhar keypoints se disponíveis
        if "keypoints" in arrow:
            draw_keypoints(img, arrow["keypoints"])
    
    # Salvar imagem
    cv2.imwrite(str(output_path), img)

def main():
    parser = argparse.ArgumentParser(
        description="Visualiza detecções dos modelos YOLO"
    )
    parser.add_argument(
        "--components",
        type=str,
        default="data/predictions/predictions_yolo.json",
        help="JSON com componentes detectados"
    )
    parser.add_argument(
        "--arrows",
        type=str,
        default="data/arrows_output/arrows_detected.json",
        help="JSON com setas detectadas"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/visualizacoes",
        help="Pasta para salvar imagens com detecções"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limita quantas imagens processar (0 = todas)"
    )
    
    args = parser.parse_args()
    
    # Carregar JSONs
    components_path = Path(args.components)
    arrows_path = Path(args.arrows)
    output_dir = Path(args.output)
    
    ensure_dir(output_dir)
    
    components_data = {}
    if components_path.exists():
        print(f"Carregando componentes: {components_path}")
        comp_json = json.loads(components_path.read_text(encoding="utf-8"))
        components_data = comp_json.get("items", {})
    else:
        print(f"AVISO: Componentes não encontrados: {components_path}")
    
    arrows_data = {}
    if arrows_path.exists():
        print(f"Carregando setas: {arrows_path}")
        arrows_json = json.loads(arrows_path.read_text(encoding="utf-8"))
        arrows_data = arrows_json.get("items", {})
    else:
        print(f"AVISO: Setas não encontradas: {arrows_path}")
    
    # Processar imagens
    all_images = set(list(components_data.keys()) + list(arrows_data.keys()))
    
    if args.limit > 0:
        all_images = list(all_images)[:args.limit]
    
    print(f"\nProcessando {len(all_images)} imagens...\n")
    
    processed = 0
    failed = 0
    
    for img_key in all_images:
        try:
            img_path = Path(img_key)
            
            if not img_path.exists():
                print(f"AVISO: Imagem não encontrada: {img_path}")
                failed += 1
                continue
            
            components = components_data.get(img_key, [])
            arrows = arrows_data.get(img_key, [])
            
            # Nome do arquivo de saída
            output_path = output_dir / f"{img_path.stem}_detected{img_path.suffix}"
            
            # Visualizar
            visualize_detections(img_path, components, arrows, output_path)
            
            processed += 1
            print(f"[{processed}/{len(all_images)}] ✓ {img_path.name} -> {output_path.name}")
            print(f"           Componentes: {len(components)}, Setas: {len(arrows)}")
            
        except Exception as e:
            failed += 1
            print(f"[{processed + failed}/{len(all_images)}] ✗ {img_key}: {e}")
    
    print(f"\n=== RESUMO ===")
    print(f"Imagens processadas: {processed}")
    print(f"Falhas: {failed}")
    print(f"Saída salva em: {output_dir}")

if __name__ == "__main__":
    main()
