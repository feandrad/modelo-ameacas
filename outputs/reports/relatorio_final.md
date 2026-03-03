# Relatório de Modelagem de Ameaças (STRIDE) — MVP

Gerado em: 2026-03-02 23:09:47

## Objetivo
Gerar automaticamente um relatório STRIDE a partir de um diagrama de arquitetura (imagem), detectando componentes com modelo supervisionado treinado no Azure Custom Vision.

---
## Diagrama: `data/imagens_validacao/imagem_1.png`

### Tampering
- **Componente**: DATABASE (tipo: database, prob: 0.9969035)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: DATABASE (tipo: database, prob: 0.98830813)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: DATABASE (tipo: database, prob: 0.9844518)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: DATABASE (tipo: database, prob: 0.60006225)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SECURITY (tipo: security, prob: 0.9794869)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SECURITY (tipo: security, prob: 0.9052315)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SECURITY (tipo: security, prob: 0.6148834)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: STORAGE (tipo: storage, prob: 0.99822253)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.9926224)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.9911361)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.989892)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.91973203)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: VPC (tipo: network, prob: 0.81875336)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: WAF (tipo: security, prob: 0.9761603)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade

### Information Disclosure
- **Componente**: DATABASE (tipo: database, prob: 0.9969035)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: DATABASE (tipo: database, prob: 0.98830813)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: DATABASE (tipo: database, prob: 0.9844518)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: DATABASE (tipo: database, prob: 0.60006225)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: monitoring (tipo: monitoring, prob: 0.9972512)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: monitoring (tipo: monitoring, prob: 0.8051842)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SECURITY (tipo: security, prob: 0.9794869)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SECURITY (tipo: security, prob: 0.9052315)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SECURITY (tipo: security, prob: 0.6148834)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SERVER (tipo: unknown, prob: 0.9808264)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: STORAGE (tipo: storage, prob: 0.99822253)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.9926224)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.9911361)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.989892)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: SUBNET_PRIVATE (tipo: network, prob: 0.91973203)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: VPC (tipo: network, prob: 0.81875336)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede
- **Componente**: WAF (tipo: security, prob: 0.9761603)
  - **Contramedidas**: criptografia em trânsito e repouso, segredos em vault, segmentação de rede

### Repudiation
- **Componente**: DATABASE (tipo: database, prob: 0.9969035)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: DATABASE (tipo: database, prob: 0.98830813)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: DATABASE (tipo: database, prob: 0.9844518)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: DATABASE (tipo: database, prob: 0.60006225)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: monitoring (tipo: monitoring, prob: 0.9972512)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: monitoring (tipo: monitoring, prob: 0.8051842)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: USER (tipo: user, prob: 0.9963356)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: USER (tipo: user, prob: 0.993298)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: USER (tipo: user, prob: 0.7366272)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos
- **Componente**: USER (tipo: user, prob: 0.72501826)
  - **Contramedidas**: logs e auditoria, trilha imutável, correlação de eventos

### Denial of Service
- **Componente**: SECURITY (tipo: security, prob: 0.9794869)
  - **Contramedidas**: rate limit, autoscaling, WAF/Shield, circuit breaker
- **Componente**: SECURITY (tipo: security, prob: 0.9052315)
  - **Contramedidas**: rate limit, autoscaling, WAF/Shield, circuit breaker
- **Componente**: SECURITY (tipo: security, prob: 0.6148834)
  - **Contramedidas**: rate limit, autoscaling, WAF/Shield, circuit breaker
- **Componente**: WAF (tipo: security, prob: 0.9761603)
  - **Contramedidas**: rate limit, autoscaling, WAF/Shield, circuit breaker

### Spoofing
- **Componente**: USER (tipo: user, prob: 0.9963356)
  - **Contramedidas**: MFA, OAuth2/OIDC, IAM least privilege, mTLS quando aplicável
- **Componente**: USER (tipo: user, prob: 0.993298)
  - **Contramedidas**: MFA, OAuth2/OIDC, IAM least privilege, mTLS quando aplicável
- **Componente**: USER (tipo: user, prob: 0.7366272)
  - **Contramedidas**: MFA, OAuth2/OIDC, IAM least privilege, mTLS quando aplicável
- **Componente**: USER (tipo: user, prob: 0.72501826)
  - **Contramedidas**: MFA, OAuth2/OIDC, IAM least privilege, mTLS quando aplicável

---
## Diagrama: `data/imagens_validacao/imagem_2.png`

### Spoofing
- **Componente**: API_GATEWAY (tipo: api, prob: 0.99788874)
  - **Contramedidas**: MFA, OAuth2/OIDC, IAM least privilege, mTLS quando aplicável
- **Componente**: API_GATEWAY (tipo: api, prob: 0.9257855)
  - **Contramedidas**: MFA, OAuth2/OIDC, IAM least privilege, mTLS quando aplicável

### Tampering
- **Componente**: API_GATEWAY (tipo: api, prob: 0.99788874)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade
- **Componente**: API_GATEWAY (tipo: api, prob: 0.9257855)
  - **Contramedidas**: TLS, validação de entrada, WAF rules, assinatura/hash de integridade

### Denial of Service
- **Componente**: API_GATEWAY (tipo: api, prob: 0.99788874)
  - **Contramedidas**: rate limit, autoscaling, WAF/Shield, circuit breaker
- **Componente**: API_GATEWAY (tipo: api, prob: 0.9257855)
  - **Contramedidas**: rate limit, autoscaling, WAF/Shield, circuit breaker

### Elevation of Privilege
- **Componente**: API_GATEWAY (tipo: api, prob: 0.99788874)
  - **Contramedidas**: least privilege, RBAC/scopes, hardening, patching
- **Componente**: API_GATEWAY (tipo: api, prob: 0.9257855)
  - **Contramedidas**: least privilege, RBAC/scopes, hardening, patching
