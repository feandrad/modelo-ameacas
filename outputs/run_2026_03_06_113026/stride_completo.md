# 🛡️ Relatório STRIDE Completo - Análise Integrada

**Gerado em**: 2026-03-06 11:30:30

## Metodologia
Este relatório integra:
1. Detecção de componentes (YOLO)
2. Detecção de setas/conexões (YOLO)
3. Análise de fluxo de dados
4. Ameaças STRIDE base + contextuais

---

## 📊 Diagrama: imagem_1.png

### Resumo
- Componentes detectados: 31
- Conexões mapeadas: 2
- Ameaças base: 23
- Ameaças contextuais: 2

### Componentes Detectados
- **SECURITY**: aws_waf
- **UNKNOWN**: aws_simple_email_service, aws_elactic_file_system(nfs)_multi-az, aws_cloud_trail, sei/sip, aws_cloud, aws_cloudfront, solr, aws_autoscaling, aws_backup, aws_rds, aws_public_subnet, aws_virtual_private_cloud, aws_cloudwatch, aws_key_management_service, aws_private_subnet, aws_elasticache, aws_application_load_balancer, aws_region
- **USER**: user

### 🔄 Fluxo de Dados
- aws_cloudfront → aws_public_subnet (confiança: 77%)
- aws_waf → aws_cloudfront (confiança: 50%)

### 🛡️ Análise STRIDE Completa
#### Spoofing (1 ameaças)
🟡 **MEDIUM**: Spoofing em user
   - Componente: user
   - Contramedidas: MFA, OAuth2/OIDC, IAM least privilege

#### Tampering (1 ameaças)
🟡 **MEDIUM**: Tampering em aws_waf
   - Componente: aws_waf
   - Contramedidas: TLS, Validação de entrada, WAF rules

#### Repudiation (1 ameaças)
🟡 **MEDIUM**: Repudiation em user
   - Componente: user
   - Contramedidas: Logs e auditoria, Trilha imutável, CloudTrail

#### Information Disclosure (21 ameaças)
🟡 **MEDIUM**: Information Disclosure em aws_cloudfront
   - Componente: aws_cloudfront
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_public_subnet
   - Componente: aws_public_subnet
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em sei/sip
   - Componente: sei/sip
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_application_load_balancer
   - Componente: aws_application_load_balancer
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_elasticache
   - Componente: aws_elasticache
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em solr
   - Componente: solr
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_simple_email_service
   - Componente: aws_simple_email_service
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_backup
   - Componente: aws_backup
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_cloudwatch
   - Componente: aws_cloudwatch
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_cloud_trail
   - Componente: aws_cloud_trail
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_key_management_service
   - Componente: aws_key_management_service
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_rds
   - Componente: aws_rds
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_elactic_file_system(nfs)_multi-az
   - Componente: aws_elactic_file_system(nfs)_multi-az
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_virtual_private_cloud
   - Componente: aws_virtual_private_cloud
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_private_subnet
   - Componente: aws_private_subnet
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_autoscaling
   - Componente: aws_autoscaling
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_waf
   - Componente: aws_waf
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_region
   - Componente: aws_region
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_cloud
   - Componente: aws_cloud
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM** [CONTEXTUAL]: Garantir criptografia em trânsito entre aws_cloudfront e aws_public_subnet
   - Componente: aws_cloudfront → aws_public_subnet
   - Contramedidas: TLS 1.3, mTLS se aplicável, VPN/PrivateLink
🟡 **MEDIUM** [CONTEXTUAL]: Garantir criptografia em trânsito entre aws_waf e aws_cloudfront
   - Componente: aws_waf → aws_cloudfront
   - Contramedidas: TLS 1.3, mTLS se aplicável, VPN/PrivateLink

#### Denial of Service (1 ameaças)
🟡 **MEDIUM**: Denial of Service em aws_waf
   - Componente: aws_waf
   - Contramedidas: Rate limit, Autoscaling, WAF/Shield

---

## 📊 Diagrama: imagem_2.png

### Resumo
- Componentes detectados: 11
- Conexões mapeadas: 3
- Ameaças base: 12
- Ameaças contextuais: 3

### Componentes Detectados
- **API**: api
- **UNKNOWN**: resource_group, sass_services, azure_services, logic_apps, developer_portal, microsoft_entra
- **USER**: user

### 🔄 Fluxo de Dados
- logic_apps → microsoft_entra (confiança: 71%)
- user → developer_portal (confiança: 70%)
- microsoft_entra → resource_group (confiança: 57%)

### 🛡️ Análise STRIDE Completa
#### Spoofing (2 ameaças)
🟡 **MEDIUM**: Spoofing em user
   - Componente: user
   - Contramedidas: MFA, OAuth2/OIDC, IAM least privilege
🟡 **MEDIUM**: Spoofing em api
   - Componente: api
   - Contramedidas: MFA, OAuth2/OIDC, IAM least privilege

#### Tampering (1 ameaças)
🟡 **MEDIUM**: Tampering em api
   - Componente: api
   - Contramedidas: TLS, Validação de entrada, WAF rules

#### Repudiation (1 ameaças)
🟡 **MEDIUM**: Repudiation em user
   - Componente: user
   - Contramedidas: Logs e auditoria, Trilha imutável, CloudTrail

#### Information Disclosure (9 ameaças)
🟡 **MEDIUM**: Information Disclosure em resource_group
   - Componente: resource_group
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em sass_services
   - Componente: sass_services
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em microsoft_entra
   - Componente: microsoft_entra
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em logic_apps
   - Componente: logic_apps
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em developer_portal
   - Componente: developer_portal
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em azure_services
   - Componente: azure_services
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM** [CONTEXTUAL]: Garantir criptografia em trânsito entre logic_apps e microsoft_entra
   - Componente: logic_apps → microsoft_entra
   - Contramedidas: TLS 1.3, mTLS se aplicável, VPN/PrivateLink
🟡 **MEDIUM** [CONTEXTUAL]: Garantir criptografia em trânsito entre user e developer_portal
   - Componente: user → developer_portal
   - Contramedidas: TLS 1.3, mTLS se aplicável, VPN/PrivateLink
🟡 **MEDIUM** [CONTEXTUAL]: Garantir criptografia em trânsito entre microsoft_entra e resource_group
   - Componente: microsoft_entra → resource_group
   - Contramedidas: TLS 1.3, mTLS se aplicável, VPN/PrivateLink

#### Denial of Service (1 ameaças)
🟡 **MEDIUM**: Denial of Service em api
   - Componente: api
   - Contramedidas: Rate limit, Autoscaling, WAF/Shield

#### Elevation of Privilege (1 ameaças)
🟡 **MEDIUM**: Elevation of Privilege em api
   - Componente: api
   - Contramedidas: Least privilege, RBAC, Hardening

---

## 📊 Diagrama: imagem_3.png

### Resumo
- Componentes detectados: 6
- Conexões mapeadas: 0
- Ameaças base: 5
- Ameaças contextuais: 0

### Componentes Detectados
- **STORAGE**: aws_amazon_simple_storage_service
- **UNKNOWN**: aws_identity_and_access_management, gcp_vertex_ai, aws_amazon_dynamodb

### 🛡️ Análise STRIDE Completa
#### Tampering (1 ameaças)
🟡 **MEDIUM**: Tampering em aws_amazon_simple_storage_service
   - Componente: aws_amazon_simple_storage_service
   - Contramedidas: TLS, Validação de entrada, WAF rules

#### Information Disclosure (4 ameaças)
🟡 **MEDIUM**: Information Disclosure em aws_amazon_dynamodb
   - Componente: aws_amazon_dynamodb
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_identity_and_access_management
   - Componente: aws_identity_and_access_management
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em gcp_vertex_ai
   - Componente: gcp_vertex_ai
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede
🟡 **MEDIUM**: Information Disclosure em aws_amazon_simple_storage_service
   - Componente: aws_amazon_simple_storage_service
   - Contramedidas: Criptografia em trânsito/repouso, Segredos em vault, Segmentação de rede

---
