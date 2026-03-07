"""
Pipeline completo: detecta componentes, setas e gera visualizações
"""
import subprocess
import sys
from pathlib import Path
import argparse

def run_command(cmd: list, description: str):
    """Executa comando e mostra progresso"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Comando: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ ERRO ao executar: {description}")
        sys.exit(1)
    
    print(f"\n✅ {description} - Concluído!")

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline completo de detecção e visualização"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="imagens_validacao",
        help="Pasta com imagens para processar"
    )
    parser.add_argument(
        "--threshold-components",
        type=float,
        default=0.5,
        help="Threshold para detecção de componentes"
    )
    parser.add_argument(
        "--threshold-arrows",
        type=float,
        default=0.3,
        help="Threshold para detecção de setas"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device: cpu, cuda, mps"
    )
    parser.add_argument(
        "--skip-components",
        action="store_true",
        help="Pula detecção de componentes (usa JSON existente)"
    )
    parser.add_argument(
        "--skip-arrows",
        action="store_true",
        help="Pula detecção de setas (usa JSON existente)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limita quantas imagens processar (0 = todas)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🎯 PIPELINE COMPLETO DE DETECÇÃO")
    print("="*60)
    print(f"Input: {args.input}")
    print(f"Device: {args.device}")
    print(f"Threshold componentes: {args.threshold_components}")
    print(f"Threshold setas: {args.threshold_arrows}")
    
    # 1. Detectar componentes
    if not args.skip_components:
        cmd = [
            sys.executable,
            "scripts/detectar_componentes_yolo.py",
            "--input", args.input,
            "--threshold", str(args.threshold_components),
            "--device", args.device
        ]
        if args.limit > 0:
            cmd.extend(["--limit", str(args.limit)])
        
        run_command(cmd, "Detectando componentes")
    else:
        print("\n⏭️  Pulando detecção de componentes (usando JSON existente)")
    
    # 2. Detectar setas
    if not args.skip_arrows:
        cmd = [
            sys.executable,
            "scripts/detectar_setas_yolo.py",
            "--input", args.input,
            "--threshold", str(args.threshold_arrows),
            "--device", args.device
        ]
        if args.limit > 0:
            cmd.extend(["--limit", str(args.limit)])
        
        run_command(cmd, "Detectando setas")
    else:
        print("\n⏭️  Pulando detecção de setas (usando JSON existente)")
    
    # 3. Gerar visualizações
    cmd = [sys.executable, "scripts/visualizar_deteccoes.py"]
    if args.limit > 0:
        cmd.extend(["--limit", str(args.limit)])
    
    run_command(cmd, "Gerando visualizações")
    
    print("\n" + "="*60)
    print("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n📁 Resultados:")
    print("   • Componentes: data/predictions/predictions_yolo.json")
    print("   • Setas: data/arrows_output/arrows_detected.json")
    print("   • Conexões: data/arrows_output/connections.json")
    print("   • Visualizações: outputs/visualizacoes/")
    print("\n")

if __name__ == "__main__":
    main()
