"""
Gera relatório STRIDE completo integrando:
- Componentes detectados (YOLO)
- Setas/conexões detectadas (YOLO)
- Análise de fluxo de dados
- Ameaças contextuais baseadas em conexões
"""
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Mapeamento Tag -> Tipo
TAG_TO_TYPE = {
    "API": "api",
    "API_GATEWAY": "api",
    "AWS_AMAZON_API_GATEWAY": "api",
    "LOAD_BALANCER": "lb",
    "AWS_APPLICATION_LOAD_BALANCER": "lb",
    "AWS_ELASTIC_LOAD_BALANCING": "lb",
    "DATABASE": "database",
    "AWS_RDS": "database",
    "AWS_AMAZON_DYNAMODB": "database",
    "AWS_DYNAMODB_TABLE": "database",
    "STORAGE": "storage",
    "AWS_SIMPLE_STORAGE_SERVICE": "storage",
    "AWS_SIMPLE_STORAGE_SERVICE_BUCKET": "storage",
    "USER": "user",
    "VPC": "network",
    "AWS_VIRTUAL_PRIVATE_CLOUD": "network",
    "AWS_PRIVATE_SUBNET": "network",
    "AWS_PUBLIC_SUBNET": "network",
    "SUBNET_PRIVATE": "network",
    "SUBNET_PUBLIC": "network",
    "WAF": "security",
    "AWS_WAF": "security",
    "SECURITY": "security",
    "MONITORING": "monitoring",
    "AWS_CLOUDWATCH": "monitoring",
}

# STRIDE por tipo
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
    "Spoofing": ["MFA", "OAuth2/OIDC", "IAM least privilege"],
    "Tampering": ["TLS", "Validação de entrada", "WAF rules", "Integridade de dados"],
    "Repudiation": ["Logs e auditoria", "Trilha imutável", "CloudTrail"],
    "Information Disclosure": ["Criptografia em trânsito/repouso", "Segredos em vault", "Segmentação de rede"],
    "Denial of Service": ["Rate limit", "Autoscaling", "WAF/Shield", "Circuit breaker"],
    "Elevation of Privilege": ["Least privilege", "RBAC", "Hardening", "Patching"],
}

def normalize_label(label):
    """Normaliza label para matching"""
    return label.upper().replace("_", " ").replace("-", " ").strip()

def tag_to_type(tag):
    """Converte tag para tipo de componente"""
    norm = normalize_label(tag)
    
    # Busca exata
    if norm in TAG_TO_TYPE:
        return TAG_TO_TYPE[norm]
    
    # Busca parcial
    for key, value in TAG_TO_TYPE.items():
        if key in norm or norm in key:
            return value
    
    return "unknown"

def load_predictions(path):
    """Carrega predições (suporta formato com/sem meta)"""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return raw.get("items", raw)

def load_connections(path):
    """Carrega conexões detectadas"""
    if not Path(path).exists():
        return {}
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return raw.get("items", raw)

def build_component_index(components):
    """Cria índice de componentes por label"""
    index = defaultdict(list)
    for comp in components:
        label = comp["label"]
        comp_type = tag_to_type(label)
        index[label].append({
            "label": label,
            "type": comp_type,
            "prob": comp.get("prob", 0)
        })
    return index

def generate_base_threats(components):
    """Gera ameaças base por componente (sem contexto de conexões)"""
    threats = []
    comp_index = build_component_index(components)
    
    for label, comps in comp_index.items():
        comp_type = comps[0]["type"]
        stride_list = STRIDE_RULES.get(comp_type, STRIDE_RULES["unknown"])
        
        for stride in stride_list:
            threats.append({
                "component": label,
                "component_type": comp_type,
                "stride": stride,
                "severity": "MEDIUM",
                "description": f"{stride} em {label}",
                "mitigations": MITIGATIONS.get(stride, []),
                "contextual": False
            })
    
    return threats

def generate_contextual_threats(connections, comp_index):
    """Gera ameaças contextuais baseadas em conexões"""
    threats = []
    
    for conn in connections:
        source = conn["from"]
        target = conn["to"]
        confidence = conn.get("confidence", 0)
        
        source_type = tag_to_type(source)
        target_type = tag_to_type(target)
        
        # USER -> DATABASE direto (CRÍTICO)
        if source_type == "user" and target_type == "database":
            threats.append({
                "component": f"{source} → {target}",
                "component_type": "connection",
                "stride": "Elevation of Privilege",
                "severity": "CRITICAL",
                "description": f"Acesso direto de usuário ao banco de dados sem camada intermediária",
                "mitigations": ["Adicionar API Gateway", "Implementar camada de aplicação", "Remover acesso direto"],
                "contextual": True,
                "connection": conn
            })
            threats.append({
                "component": f"{source} → {target}",
                "component_type": "connection",
                "stride": "Information Disclosure",
                "severity": "CRITICAL",
                "description": f"Dados sensíveis expostos por acesso direto ao banco",
                "mitigations": ["Criptografia end-to-end", "Mascaramento de dados", "Adicionar proxy"],
                "contextual": True,
                "connection": conn
            })
        
        # USER -> API/LB (sem WAF)
        if source_type == "user" and target_type in ["api", "lb"]:
            # Verificar se existe WAF no caminho
            has_waf = any(tag_to_type(c["from"]) == "security" or tag_to_type(c["to"]) == "security" 
                         for c in connections)
            
            if not has_waf:
                threats.append({
                    "component": f"{source} → {target}",
                    "component_type": "connection",
                    "stride": "Tampering",
                    "severity": "HIGH",
                    "description": f"Conexão externa sem WAF - vulnerável a ataques",
                    "mitigations": ["Adicionar WAF", "Rate limiting", "DDoS protection"],
                    "contextual": True,
                    "connection": conn
                })
        
        # API -> DATABASE (sem validação)
        if source_type == "api" and target_type == "database":
            threats.append({
                "component": f"{source} → {target}",
                "component_type": "connection",
                "stride": "Tampering",
                "severity": "HIGH",
                "description": f"Risco de SQL Injection na conexão API-Database",
                "mitigations": ["Prepared statements", "ORM", "Validação de entrada", "Least privilege DB user"],
                "contextual": True,
                "connection": conn
            })
            threats.append({
                "component": f"{source} → {target}",
                "component_type": "connection",
                "stride": "Information Disclosure",
                "severity": "MEDIUM",
                "description": f"Conexão API-Database deve usar criptografia",
                "mitigations": ["TLS para conexão DB", "Secrets Manager", "Rotação de credenciais"],
                "contextual": True,
                "connection": conn
            })
        
        # Qualquer conexão sem criptografia assumida
        threats.append({
            "component": f"{source} → {target}",
            "component_type": "connection",
            "stride": "Information Disclosure",
            "severity": "MEDIUM",
            "description": f"Garantir criptografia em trânsito entre {source} e {target}",
            "mitigations": ["TLS 1.3", "mTLS se aplicável", "VPN/PrivateLink"],
            "contextual": True,
            "connection": conn
        })
    
    return threats

def generate_markdown_report(img_name, components, connections, base_threats, contextual_threats):
    """Gera relatório em Markdown"""
    md = []
    
    md.append(f"## 📊 Diagrama: {img_name}")
    md.append("")
    
    # Resumo
    md.append("### Resumo")
    md.append(f"- Componentes detectados: {len(components)}")
    md.append(f"- Conexões mapeadas: {len(connections)}")
    md.append(f"- Ameaças base: {len(base_threats)}")
    md.append(f"- Ameaças contextuais: {len(contextual_threats)}")
    md.append("")
    
    # Componentes
    md.append("### Componentes Detectados")
    comp_by_type = defaultdict(list)
    for comp in components:
        comp_type = tag_to_type(comp["label"])
        comp_by_type[comp_type].append(comp["label"])
    
    for comp_type in sorted(comp_by_type.keys()):
        labels = comp_by_type[comp_type]
        md.append(f"- **{comp_type.upper()}**: {', '.join(set(labels))}")
    md.append("")
    
    # Fluxo de dados
    if connections:
        md.append("### 🔄 Fluxo de Dados")
        for conn in connections:
            conf = conn.get("confidence", 0)
            md.append(f"- {conn['from']} → {conn['to']} (confiança: {conf:.0%})")
        md.append("")
    
    # Ameaças CRÍTICAS (contextuais)
    critical = [t for t in contextual_threats if t["severity"] == "CRITICAL"]
    if critical:
        md.append("### 🚨 AMEAÇAS CRÍTICAS")
        for t in critical:
            md.append(f"#### {t['stride']}: {t['description']}")
            md.append(f"**Componente**: {t['component']}")
            md.append(f"**Contramedidas**:")
            for m in t["mitigations"]:
                md.append(f"- {m}")
            md.append("")
    
    # Ameaças por STRIDE
    md.append("### 🛡️ Análise STRIDE Completa")
    
    all_threats = base_threats + contextual_threats
    by_stride = defaultdict(list)
    for t in all_threats:
        by_stride[t["stride"]].append(t)
    
    for stride in ["Spoofing", "Tampering", "Repudiation", "Information Disclosure", 
                   "Denial of Service", "Elevation of Privilege"]:
        if stride not in by_stride:
            continue
        
        threats = by_stride[stride]
        md.append(f"#### {stride} ({len(threats)} ameaças)")
        
        # Agrupar por severidade
        by_sev = defaultdict(list)
        for t in threats:
            by_sev[t["severity"]].append(t)
        
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if sev not in by_sev:
                continue
            
            for t in by_sev[sev]:
                icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡"
                ctx = " [CONTEXTUAL]" if t.get("contextual") else ""
                md.append(f"{icon} **{sev}**{ctx}: {t['description']}")
                md.append(f"   - Componente: {t['component']}")
                if t["mitigations"]:
                    md.append(f"   - Contramedidas: {', '.join(t['mitigations'][:3])}")
        md.append("")
    
    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="Gera relatório STRIDE completo com análise de fluxo")
    parser.add_argument("--components", type=str, default="data/predictions/predictions_yolo.json")
    parser.add_argument("--connections", type=str, default="data/arrows_output/connections.json")
    parser.add_argument("--out-md", type=str, default="outputs/reports/stride_completo.md")
    parser.add_argument("--out-json", type=str, default="data/modelo_ameacas/threat_model_completo.json")
    args = parser.parse_args()
    
    # Carregar dados
    components_data = load_predictions(args.components)
    connections_data = load_connections(args.connections)
    
    # Processar cada imagem
    all_results = {}
    md_parts = []
    
    md_parts.append("# 🛡️ Relatório STRIDE Completo - Análise Integrada")
    md_parts.append("")
    md_parts.append(f"**Gerado em**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_parts.append("")
    md_parts.append("## Metodologia")
    md_parts.append("Este relatório integra:")
    md_parts.append("1. Detecção de componentes (YOLO)")
    md_parts.append("2. Detecção de setas/conexões (YOLO)")
    md_parts.append("3. Análise de fluxo de dados")
    md_parts.append("4. Ameaças STRIDE base + contextuais")
    md_parts.append("")
    md_parts.append("---")
    md_parts.append("")
    
    for img_path, components in components_data.items():
        img_name = Path(img_path).name
        connections = connections_data.get(img_path, [])
        
        # Gerar ameaças
        base_threats = generate_base_threats(components)
        
        comp_index = build_component_index(components)
        contextual_threats = generate_contextual_threats(connections, comp_index)
        
        # Relatório
        md_report = generate_markdown_report(
            img_name, components, connections, 
            base_threats, contextual_threats
        )
        md_parts.append(md_report)
        md_parts.append("---")
        md_parts.append("")
        
        # Salvar JSON
        all_results[img_path] = {
            "components": components,
            "connections": connections,
            "base_threats": base_threats,
            "contextual_threats": contextual_threats,
            "summary": {
                "total_components": len(components),
                "total_connections": len(connections),
                "total_base_threats": len(base_threats),
                "total_contextual_threats": len(contextual_threats),
                "critical_threats": len([t for t in contextual_threats if t["severity"] == "CRITICAL"])
            }
        }
    
    # Salvar arquivos
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(md_parts), encoding="utf-8")
    
    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_json).write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    print("✅ Relatório STRIDE completo gerado")
    print(f"   Markdown: {args.out_md}")
    print(f"   JSON: {args.out_json}")
    
    # Estatísticas
    total_imgs = len(all_results)
    total_comps = sum(r["summary"]["total_components"] for r in all_results.values())
    total_conns = sum(r["summary"]["total_connections"] for r in all_results.values())
    total_threats = sum(r["summary"]["total_base_threats"] + r["summary"]["total_contextual_threats"] 
                       for r in all_results.values())
    total_critical = sum(r["summary"]["critical_threats"] for r in all_results.values())
    
    print(f"\n📊 Estatísticas:")
    print(f"   Imagens: {total_imgs}")
    print(f"   Componentes: {total_comps}")
    print(f"   Conexões: {total_conns}")
    print(f"   Ameaças totais: {total_threats}")
    print(f"   Ameaças críticas: {total_critical}")

if __name__ == "__main__":
    main()
