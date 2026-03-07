"""
Script de teste rápido para verificar se a visualização está funcionando
"""
import sys
from pathlib import Path

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...\n")
    
    missing = []
    
    try:
        import cv2
        print("✅ opencv-python instalado")
    except ImportError:
        print("❌ opencv-python NÃO instalado")
        missing.append("opencv-python")
    
    try:
        import numpy
        print("✅ numpy instalado")
    except ImportError:
        print("❌ numpy NÃO instalado")
        missing.append("numpy")
    
    try:
        from ultralytics import YOLO
        print("✅ ultralytics instalado")
    except ImportError:
        print("❌ ultralytics NÃO instalado")
        missing.append("ultralytics")
    
    try:
        import torch
        print("✅ torch instalado")
    except ImportError:
        print("❌ torch NÃO instalado")
        missing.append("torch")
    
    if missing:
        print(f"\n⚠️  Dependências faltando: {', '.join(missing)}")
        print("\nInstale com:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✅ Todas as dependências estão instaladas!")
    return True

def check_models():
    """Verifica se os modelos existem"""
    print("\n🔍 Verificando modelos...\n")
    
    models_dir = Path("models")
    icons_model = models_dir / "best_icons.pt"
    arrows_model = models_dir / "best_arrows.pt"
    
    all_ok = True
    
    if icons_model.exists():
        size_mb = icons_model.stat().st_size / (1024 * 1024)
        print(f"✅ best_icons.pt encontrado ({size_mb:.1f} MB)")
    else:
        print(f"❌ best_icons.pt NÃO encontrado em {icons_model}")
        all_ok = False
    
    if arrows_model.exists():
        size_mb = arrows_model.stat().st_size / (1024 * 1024)
        print(f"✅ best_arrows.pt encontrado ({size_mb:.1f} MB)")
    else:
        print(f"❌ best_arrows.pt NÃO encontrado em {arrows_model}")
        all_ok = False
    
    if not all_ok:
        print("\n⚠️  Modelos faltando! Certifique-se que estão na pasta models/")
        return False
    
    print("\n✅ Todos os modelos estão presentes!")
    return True

def check_images():
    """Verifica se há imagens para processar"""
    print("\n🔍 Verificando imagens...\n")
    
    images_dir = Path("imagens_validacao")
    
    if not images_dir.exists():
        print(f"❌ Pasta {images_dir} não encontrada")
        return False
    
    exts = {".png", ".jpg", ".jpeg"}
    images = [f for f in images_dir.iterdir() if f.suffix.lower() in exts]
    
    if not images:
        print(f"❌ Nenhuma imagem encontrada em {images_dir}")
        return False
    
    print(f"✅ {len(images)} imagens encontradas:")
    for img in images[:5]:  # Mostrar apenas as 5 primeiras
        print(f"   • {img.name}")
    if len(images) > 5:
        print(f"   ... e mais {len(images) - 5} imagens")
    
    return True

def check_scripts():
    """Verifica se os scripts existem"""
    print("\n🔍 Verificando scripts...\n")
    
    scripts = [
        "scripts/detectar_componentes_yolo.py",
        "scripts/detectar_setas_yolo.py",
        "scripts/visualizar_deteccoes.py",
        "scripts/pipeline_completo.py"
    ]
    
    all_ok = True
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} NÃO encontrado")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Alguns scripts estão faltando!")
        return False
    
    print("\n✅ Todos os scripts estão presentes!")
    return True

def main():
    print("="*60)
    print("🧪 TESTE DE CONFIGURAÇÃO - VISUALIZAÇÃO DE DETECÇÕES")
    print("="*60)
    
    checks = [
        ("Dependências", check_dependencies),
        ("Modelos", check_models),
        ("Imagens", check_images),
        ("Scripts", check_scripts)
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✅ OK" if result else "❌ FALHOU"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 TUDO PRONTO! Você pode executar:")
        print("\n   python scripts/pipeline_completo.py\n")
        print("Ou para testar com uma imagem:")
        print("\n   python scripts/pipeline_completo.py --limit 1\n")
    else:
        print("⚠️  CONFIGURAÇÃO INCOMPLETA")
        print("\nResolva os problemas acima antes de continuar.")
        print("\nPara instalar dependências:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
