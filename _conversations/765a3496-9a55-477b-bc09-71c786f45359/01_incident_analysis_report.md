# 🔴 INCIDENT ANALYSIS REPORT
## Remita Payment Platform — Unauthorized Data Exfiltration
**Classification:** CRITICAL — TLP:RED  
**Date of Discovery:** April 4, 2026  
**Incident Reference:** REMITA-BREACH-2026-04  
**Analyst:** Threat Intelligence Unit  
**Status:** Active / Uncontained

---

## Executive Summary

On April 4, 2026, a threat actor operating under the alias **"bytetobreach"** published a forum post on a known dark web marketplace claiming to have exfiltrated approximately **3 terabytes of data** from **Remita**, Nigeria's largest government payment processing platform operated by SystemSpecs. The dump includes KYC identity documents, full database backups, source code, cryptographic keys, and administrative credentials.

> [!CAUTION]
> This breach potentially affects **every Nigerian citizen, business, and government entity** that has transacted through the Remita platform — including TSA (Treasury Single Account) federal collections, state government payments, salary disbursements, and tax remittances.

---

## 1. Threat Actor Profile

| Attribute | Detail |
|---|---|
| **Alias** | bytetobreach |
| **Forum Rank** | Com Boss |
| **Account Created** | March 2026 |
| **Posts** | 5 |
| **Threads** | 4 |
| **Credits** | 45 |
| **Hosting** | DarkWebInformer-indexed forum |

> [!NOTE]
> The account is relatively new (March 2026) with low post count but high-impact threads, suggesting a purpose-built account for this specific operation or a seasoned actor using a fresh identity.

---

## 2. Evidence — Forum Post

![Forum post by bytetobreach on dark web marketplace claiming Remita full data dump](C:\Users\OMEN\.gemini\antigravity\brain\765a3496-9a55-477b-bc09-71c786f45359\forum_post.jpg)

### Claimed Data Categories

| Dump File | Type | Description |
|---|---|---|
| `PASSPORTS.png` | KYC | Passport photos and scanned ID documents |
| `DATABASE_RESTORE.png` | Database | Full MySQL/PostgreSQL database backup |
| `SOURCE_CODES.png` | Source Code | Remita application source code |
| `SECRETS_LEAKS.png` | Credentials | API keys, secrets, tokens, environment variables |
| `GOV_HSM_KEYS.png` | Cryptographic | Government Hardware Security Module signing keys |
| `GITKRAKEN_TO_S3.png` | DevOps | Git commit history and artifacts pushed to S3 |

### Attacker's Claims (Verbatim)
- *"Around 3TB of S3 storage was accessed, from which +800GB was only KYC related services"*
- *"The rest is MySQL / Postgres databases, and a lot of logs and docker registries"*
- *"KYC documents are huge, and comprises many types of documents: ID's, Passports, Photos, Bank statement, Electricity bills, etc."*
- *"I put for free the source codes, +35,000k passwords hashes, and three databases"*
- *"All of this is happening, thanks to Sterling Bank of niggaland. Their servers were very helpful in conducting the attacks on Remita."*

### Distribution Method
- VPS direct access link (expected TTL: <24 hours)
- 3 backup mirror links
- Contact information provided for private data sales

---

## 3. Evidence — Exposed KYC Documents

![Exposed Nigerian KYC documents including driver's licenses, voter's cards, and passports](C:\Users\OMEN\.gemini\antigravity\brain\765a3496-9a55-477b-bc09-71c786f45359\kyc_documents.jpg)

### Document Types Identified
- **National Driver's Licenses** — Full names, DOB, addresses, photos, license classes
- **INEC Voter's Cards** — Names, polling units, registration details
- **Nigerian International Passports** — Full biometric photos and personal data
- **Utility Bills** — Address confirmation documents
- **Bank Statements** — Financial activity records

> [!WARNING]
> All visible documents are **fully unredacted** with complete PII exposed. At 800GB+ of KYC data, the potential number of affected individuals is in the **tens of millions**.

---

## 4. Evidence — Database Exposure

![Database tables showing Business Owner, Interbanking, Admins, and Personal Info data](C:\Users\OMEN\.gemini\antigravity\brain\765a3496-9a55-477b-bc09-71c786f45359\database_tables.jpg)

### Exposed Database Categories

| Category | Risk Level | Contents |
|---|---|---|
| **BUSINESS OWNER** | 🔴 Critical | Business registration records with Base64 + GZIP encoded documents |
| **INTERBANKING** | 🔴 Critical | Inter-bank transaction routing, settlement data, bank-to-bank transfer records |
| **ADMINS** | 🔴 Critical | Administrative user accounts, hashed passwords, privilege levels |
| **PERSONAL INFOS** | 🔴 Critical | Customer PII — names, addresses, phone numbers, BVN references |

> [!IMPORTANT]
> The note "UPLOADED DOCUMENTS ARE BASE64 > GZIP ENCODED" confirms these are **raw production database tables**, not sanitized exports. The encoding is the application-level storage format, meaning the attacker has the original data in its native form.

---

## 5. Attack Vector Analysis

### Probable Initial Access
Based on the evidence:
1. **S3 Bucket Misconfiguration** — 3TB extracted from S3 suggests overly permissive bucket policies or leaked IAM credentials
2. **Sterling Bank Pivot** — The attacker explicitly credits Sterling Bank infrastructure as an attack vector, suggesting either:
   - Compromised API credentials from Sterling Bank's Remita integration
   - Lateral movement through the inter-bank network
   - Abuse of a trusted VPN/network pathway between institutions
3. **Git History Exposure** — `GITKRAKEN_TO_S3.png` indicates developer credentials or CI/CD pipelines were compromised, allowing S3 access via committed secrets

### MITRE ATT&CK Mapping

| Tactic | Technique | Evidence |
|---|---|---|
| Initial Access | T1078 — Valid Accounts | Possible Sterling Bank credential abuse |
| Collection | T1530 — Data from Cloud Storage | 3TB S3 exfiltration |
| Exfiltration | T1567 — Exfiltration Over Web Service | Data moved to attacker VPS |
| Credential Access | T1552.001 — Credentials in Files | Source code secrets leak |
| Impact | T1486 — Data Exfiltration for Extortion | Public dump with backup mirrors |
| Persistence | T1098 — Account Manipulation | Admin credential database exposure |

---

## 6. Severity Assessment

### CVSS-like Scoring

| Factor | Score | Justification |
|---|---|---|
| Confidentiality Impact | **10/10** | Complete KYC, financial, and cryptographic data exposed |
| Integrity Impact | **9/10** | Admin credentials + source code = potential system manipulation |
| Availability Impact | **7/10** | HSM key compromise may force infrastructure rotation |
| Scope | **10/10** | National-scale: government, banks, businesses, citizens |
| Exploitability | **9/10** | Data already publicly accessible with mirrors |
| **Overall Severity** | **🔴 CRITICAL** | National-scale financial infrastructure compromise |

---

## 7. Affected Entities

### Primary
- **SystemSpecs (Remita operator)**
- **Central Bank of Nigeria (CBN)** — TSA infrastructure
- **All 36 State Governments + FCT** — Payment processing
- **774 LGAs** — Revenue collection
- **Sterling Bank** — Named pivot point

### Secondary
- **All Nigerian banks** integrated with Remita's interbanking layer
- **Federal MDAs** — Salary, pension, and vendor payments
- **NIBSS** — Potential downstream impact on NIP/NIBSS Instant Payment
- **Millions of Nigerian citizens** — KYC data exposed

---

## 8. Regulatory & Legal Framework

| Regulator | Relevant Law/Regulation | Obligation |
|---|---|---|
| **NDPC** (Nigeria Data Protection Commission) | NDPA 2023 | Mandatory 72-hour breach notification |
| **CBN** | Risk-Based Cybersecurity Framework 2022 | Immediate incident reporting to CBN |
| **NCC** | Cybercrimes Act 2015 | Criminal investigation referral |
| **NITDA** | NITDA Act 2007 | Technology infrastructure incident reporting |
| **EFCC** | Money Laundering (Prevention) Act | Financial crime investigation if funds at risk |

---

## 9. Recommended Immediate Actions

1. **Hour 0-4:** CBN and NDPC formal incident notification
2. **Hour 0-8:** Revoke all AWS IAM credentials and rotate S3 access keys
3. **Hour 0-12:** Force password reset for all administrative accounts
4. **Hour 0-24:** Invalidate and re-issue all HSM keys and signing certificates
5. **Hour 0-24:** Forensic acquisition of Sterling Bank integration logs
6. **Day 1-3:** Full source code audit for embedded secrets (truffleHog/git-secrets)
7. **Day 1-7:** Public disclosure to affected data subjects per NDPA requirements
8. **Day 1-14:** Engage external incident response firm (e.g., CrowdStrike, Mandiant)

---

*Report prepared for internal threat intelligence and regulatory coordination purposes. Distribution limited to authorized personnel.*
