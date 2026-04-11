# 🛡️ REMEDIATION & HARDENING CHECKLIST
## For Organizations Integrated with Remita Payment Platform
**Date:** April 4, 2026  
**Applies To:** All entities with Remita API integrations, payment gateway dependencies, or shared authentication infrastructure  
**Priority:** IMMEDIATE

---

## ✅ Phase 1: Emergency Response (0-24 Hours)

### Credential Rotation
- [ ] Rotate ALL Remita API keys (production and staging)
- [ ] Rotate all AWS IAM credentials if using shared S3 infrastructure
- [ ] Change all administrative passwords on payment gateway interfaces
- [ ] Revoke and re-issue any OAuth tokens or JWT signing keys used with Remita
- [ ] Revoke all SSH keys that may have been used to access Remita-adjacent infrastructure
- [ ] Rotate database connection strings if any databases were shared or co-hosted

### Access Control
- [ ] Enable MFA on ALL administrative accounts immediately
- [ ] Disable any service accounts with static credentials pending rotation
- [ ] Review and restrict IP allowlists on payment API endpoints
- [ ] Audit active sessions and force logout all admin users
- [ ] Revoke VPN access for any shared network pathways with Remita

### Monitoring
- [ ] Enable enhanced logging on all payment transaction endpoints
- [ ] Set up real-time alerts for:
  - [ ] Unusual payment amounts or frequencies
  - [ ] New admin account creation
  - [ ] API calls from unrecognized IP addresses
  - [ ] Database queries against employee/customer PII tables
  - [ ] Failed authentication attempts exceeding threshold
- [ ] Monitor dark web forums for your organization's data in the dump

---

## ✅ Phase 2: Forensic Assessment (24-72 Hours)

### Transaction Audit
- [ ] Review ALL payment transactions for the last 90 days
- [ ] Flag transactions with mismatched beneficiary details
- [ ] Cross-reference outgoing payments against approved budget/payroll
- [ ] Check for duplicate or reversed transactions that were re-initiated
- [ ] Verify bank account details for all recurring payment beneficiaries

### Infrastructure Audit
- [ ] Scan all servers for indicators of compromise (IOCs):
  - [ ] Unexpected cron jobs or scheduled tasks
  - [ ] Unknown SSH authorized keys
  - [ ] Modified system binaries
  - [ ] Unusual outbound network connections
- [ ] Audit S3 bucket policies and access logs
- [ ] Review CloudTrail / Azure Activity Logs for unauthorized access
- [ ] Check Docker registries for tampered images
- [ ] Audit Git repositories for committed secrets (use `truffleHog` or `git-secrets`)

### Identity Verification
- [ ] Verify employee/staff BVN records against known-good master lists
- [ ] Cross-check vendor bank account details with registration documents
- [ ] Audit pension recipient identities against biometric records
- [ ] Flag any recently changed bank account details for manual verification

---

## ✅ Phase 3: Hardening (1-2 Weeks)

### Network Security
- [ ] Implement network segmentation between payment systems and general IT
- [ ] Deploy Web Application Firewall (WAF) on all payment endpoints
- [ ] Enable TLS 1.3 minimum on all inter-system communications
- [ ] Implement certificate pinning for critical API integrations
- [ ] Review and harden firewall rules — deny-all default policy

### Application Security
- [ ] Conduct source code review of all Remita integration code
- [ ] Remove hardcoded credentials from configuration files
- [ ] Implement secrets management (HashiCorp Vault, AWS Secrets Manager)
- [ ] Enable parameterized queries to prevent SQL injection
- [ ] Implement rate limiting on all authentication endpoints
- [ ] Deploy CSRF/XSS protections on all web interfaces

### Data Protection
- [ ] Encrypt all PII at rest (AES-256 minimum)
- [ ] Implement field-level encryption for sensitive data (BVN, account numbers)
- [ ] Enable database audit logging for all PII table access
- [ ] Implement data loss prevention (DLP) monitoring
- [ ] Review and enforce data retention policies — purge unnecessary KYC copies
- [ ] Implement tokenization for stored payment credentials

### Cryptographic Security
- [ ] Verify HSM key integrity — compare against known-good key fingerprints
- [ ] Rotate all signing certificates used for payment authorization
- [ ] Implement key escrow with dual-control procedures
- [ ] Deploy certificate transparency monitoring
- [ ] Enable DNSSEC for all payment-related domains

---

## ✅ Phase 4: Governance & Compliance (2-4 Weeks)

### Regulatory Notification
- [ ] File breach notification with NDPC within 72 hours (NDPA 2023 requirement)
- [ ] Notify CBN per Risk-Based Cybersecurity Framework
- [ ] Notify affected data subjects with clear, actionable guidance
- [ ] Document incident timeline for regulatory evidence
- [ ] Engage legal counsel for liability assessment

### Policy Updates
- [ ] Update incident response plan with lessons learned
- [ ] Implement mandatory 90-day credential rotation policy
- [ ] Establish vendor security assessment program for payment integrations
- [ ] Create data breach communication template for future incidents
- [ ] Define clear escalation matrix for cybersecurity incidents

### Third-Party Risk Management
- [ ] Request SOC 2 Type II report from SystemSpecs/Remita
- [ ] Review all third-party integrations for shared credential exposure
- [ ] Implement vendor risk scoring for critical payment dependencies
- [ ] Establish contractual SLAs for breach notification from vendors
- [ ] Conduct tabletop exercise simulating payment system compromise

---

## ✅ Phase 5: Continuous Improvement (Ongoing)

### Monitoring & Detection
- [ ] Deploy SIEM solution with payment-specific detection rules
- [ ] Implement User and Entity Behavior Analytics (UEBA)
- [ ] Subscribe to threat intelligence feeds covering Nigerian financial sector
- [ ] Conduct regular penetration testing (quarterly minimum)
- [ ] Implement bug bounty program for payment infrastructure

### Staff & Awareness
- [ ] Conduct emergency cybersecurity briefing for all finance/IT staff
- [ ] Implement phishing simulation training
- [ ] Establish secure communication channels for incident reporting
- [ ] Train on recognizing social engineering using stolen PII

---

> [!TIP]
> **Quick Wins:** The three most impactful actions you can take right now:
> 1. **Rotate ALL Remita API keys** — eliminates credential reuse risk
> 2. **Enable MFA everywhere** — blocks credential stuffing from leaked password hashes
> 3. **Audit last 90 days of payments** — detects any exploitation that may have already occurred
