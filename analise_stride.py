"""
Script orquestrador para análise STRIDE completa
Executa o pipeline em ordem: componentes → setas → STRIDE
"""
import argparse
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


def run_command(cmd, description):
    """Executa comando e mostra progresso"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Comando: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ ERRO ao executar: {description}")
        sys.exit(1)
    
    print(f"\n✅ {description} - Concluído")
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Executa pipeline completo de análise STRIDE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Básico (usa defaults)
  python analise_stride.py

  # Customizado
  python analise_stride.py \\
    --input minhas_imagens/ \\
    --icons-threshold 0.6 \\
    --arrows-threshold 0.4 \\
    --device mps

  # Apenas componentes e setas (sem STRIDE)
  python analise_stride.py --skip-stride

  # Apenas STRIDE (assume que já rodou detecções)
  python analise_stride.py --only-stride
  
  # Usar pasta de output específica
  python analise_stride.py --output-dir outputs/run_2026_03_06_143022
        """
    )
    
    # Inputs
    parser.add_argument(
        "--input",
        type=str,
        default="imagens_validacao",
        help="Pasta com imagens para analisar (default: imagens_validacao)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Pasta de saída para esta execução (default: outputs/run_TIMESTAMP)"
    )
    
    # Modelos
    parser.add_argument(
        "--icons-model",
        type=str,
        default="models/best_icons.pt",
        help="Modelo YOLO de componentes (default: models/best_icons.pt)"
    )
    parser.add_argument(
        "--arrows-model",
        type=str,
        default="models/best_arrows.pt",
        help="Modelo YOLO de setas (default: models/best_arrows.pt)"
    )
    
    # Thresholds
    parser.add_argument(
        "--icons-threshold",
        type=float,
        default=0.5,
        help="Confiança mínima para componentes (default: 0.5)"
    )
    parser.add_argument(
        "--arrows-threshold",
        type=float,
        default=0.3,
        help="Confiança mínima para setas (default: 0.3)"
    )
    
    # Outputs (serão sobrescritos se --output-dir for usado)
    parser.add_argument(
        "--out-components",
        type=str,
        default=None,
        help="Saída de componentes (default: <output-dir>/predictions_yolo.json)"
    )
    parser.add_argument(
        "--out-arrows",
        type=str,
        default=None,
        help="Saída de setas (default: <output-dir>/arrows_detected.json)"
    )
    parser.add_argument(
        "--out-connections",
        type=str,
        default=None,
        help="Saída de conexões (default: <output-dir>/connections.json)"
    )
    parser.add_argument(
        "--out-stride-md",
        type=str,
        default=None,
        help="Relatório STRIDE (default: <output-dir>/stride_completo.md)"
    )
    parser.add_argument(
        "--out-stride-json",
        type=str,
        default=None,
        help="JSON STRIDE (default: <output-dir>/threat_model_completo.json)"
    )
    
    # Configurações
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda", "mps"],
        help="Device para inferência (default: cpu)"
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=50,
        help="Tolerância em pixels para mapear conexões (default: 50)"
    )
    
    # Controle de fluxo
    parser.add_argument(
        "--skip-components",
        action="store_true",
        help="Pula detecção de componentes (usa arquivo existente)"
    )
    parser.add_argument(
        "--skip-arrows",
        action="store_true",
        help="Pula detecção de setas (usa arquivo existente)"
    )
    parser.add_argument(
        "--skip-stride",
        action="store_true",
        help="Pula geração do relatório STRIDE"
    )
    parser.add_argument(
        "--only-stride",
        action="store_true",
        help="Executa apenas geração STRIDE (assume detecções já feitas)"
    )
    
    args = parser.parse_args()
    
    # Criar pasta de output com timestamp
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        args.output_dir = f"outputs/run_{timestamp}"
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Definir caminhos de saída padrão se não especificados
    if args.out_components is None:
        args.out_components = str(output_dir / "predictions_yolo.json")
    if args.out_arrows is None:
        args.out_arrows = str(output_dir / "arrows_detected.json")
    if args.out_connections is None:
        args.out_connections = str(output_dir / "connections.json")
    if args.out_stride_md is None:
        args.out_stride_md = str(output_dir / "stride_completo.md")
    if args.out_stride_json is None:
        args.out_stride_json = str(output_dir / "threat_model_completo.json")
    
    # Validações
    if not Path(args.input).exists():
        print(f"❌ Pasta de entrada não encontrada: {args.input}")
        sys.exit(1)
    
    if not args.skip_components and not args.only_stride:
        if not Path(args.icons_model).exists():
            print(f"❌ Modelo de ícones não encontrado: {args.icons_model}")
            sys.exit(1)
    
    if not args.skip_arrows and not args.only_stride:
        if not Path(args.arrows_model).exists():
            print(f"❌ Modelo de setas não encontrado: {args.arrows_model}")
            sys.exit(1)
    
    # Banner
    print("\n" + "="*60)
    print("🛡️  ANÁLISE STRIDE - Pipeline Completo")
    print("="*60)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Imagens: {args.input}")
    print(f"Output: {args.output_dir}")
    print(f"Device: {args.device}")
    print("="*60)
    
    # Determinar o executável Python correto (usa o mesmo do processo atual)
    python_exe = sys.executable
    
    # Etapa 1: Detectar Componentes
    if not args.skip_components and not args.only_stride:
        cmd_components = [
            python_exe,
            "scripts/detectar_componentes_yolo.py",
            "--model", args.icons_model,
            "--input", args.input,
            "--out", args.out_components,
            "--threshold", str(args.icons_threshold),
            "--device", args.device
        ]
        run_command(cmd_components, "Etapa 1/3: Detectar Componentes")
    else:
        print(f"\n⏭️  Pulando detecção de componentes (usando {args.out_components})")
    
    # Etapa 2: Detectar Setas
    if not args.skip_arrows and not args.only_stride:
        cmd_arrows = [
            python_exe,
            "scripts/detectar_setas_yolo.py",
            "--model", args.arrows_model,
            "--input", args.input,
            "--components", args.out_components,
            "--out", args.out_arrows,
            "--out-connections", args.out_connections,
            "--threshold", str(args.arrows_threshold),
            "--device", args.device,
            "--tolerance", str(args.tolerance)
        ]
        run_command(cmd_arrows, "Etapa 2/3: Detectar Setas e Mapear Conexões")
    else:
        print(f"\n⏭️  Pulando detecção de setas (usando {args.out_connections})")
    
    # Etapa 3: Gerar STRIDE
    if not args.skip_stride:
        cmd_stride = [
            python_exe,
            "scripts/gerar_stride_completo.py",
            "--components", args.out_components,
            "--connections", args.out_connections,
            "--out-md", args.out_stride_md,
            "--out-json", args.out_stride_json
        ]
        run_command(cmd_stride, "Etapa 3/3: Gerar Relatório STRIDE")
    else:
        print(f"\n⏭️  Pulando geração STRIDE")
    
    # Resumo final
    print("\n" + "="*60)
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n📁 Pasta de saída: {args.output_dir}")
    print("\n📄 Arquivos gerados:")
    
    if not args.skip_components and not args.only_stride:
        print(f"  • {Path(args.out_components).name}")
    if not args.skip_arrows and not args.only_stride:
        print(f"  • {Path(args.out_arrows).name}")
        print(f"  • {Path(args.out_connections).name}")
    if not args.skip_stride:
        print(f"  • {Path(args.out_stride_md).name}")
        print(f"  • {Path(args.out_stride_json).name}")
    
    print("\n📊 Próximos passos:")
    print(f"  • Ver relatório: cat {args.out_stride_md}")
    print(f"  • Ver JSON: cat {args.out_stride_json}")
    print(f"  • Listar runs: ls -lt outputs/")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
