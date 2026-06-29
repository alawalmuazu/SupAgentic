$prompt = @"
You are a senior penetration tester with 15+ years experience. Perform a COMPREHENSIVE vulnerability and penetration testing analysis on the following target: VeriPay Nigeria (veripay.ng / veripaysuite.com) - a Nigerian HR, payroll and biometric payment management SaaS platform.

## Target Intelligence Gathered:

### Platform Architecture
- veripay.ng: Vue.js FRONTEND (RUNNING IN DEVELOPMENT MODE - detected), routes: /Form, /Resume, /Login/logout, /Validations/resetPassword
- veripaysuite.com: Marketing site + SaaS portal
- veripaysuite.com/enugu/: Legacy PHP system (AppMart Integrated Ltd © 2013) - state government payroll for Enugu State
- veripaysuite.com/crs/: Legacy PHP system (AppMart Integrated Ltd © 2015) - state government payroll for Cross River State  
- veripaysuite.com/veripaysub/Auth/login: Newer subscription management portal
- Framework: CodeIgniter (PHP) suspected for backend, Vue.js for frontend SPA
- Interswitch payment gateway integration
- BVN (Bank Verification Number) and NUBAN validation
- Biometric fingerprint system integration

### Exposed Endpoints Found
1. https://veripay.ng/ - Main login (Email/Phone + password)
2. https://veripay.ng/Form - Company subscription form (13-step wizard)
3. https://veripay.ng/Resume - Public job listing (integer IDs: /apply/1 through /apply/11)
4. https://veripay.ng/Resume/apply/{id} - Job application forms (IDOR candidate - ID 1,3 show epoch date 01-Jan-1970)
5. https://veripay.ng/Validations/resetPassword - Password reset
6. https://veripay.ng/Login/logout - Logout endpoint
7. https://veripay.ng/index.php/Form/home - Form home (reveals CodeIgniter index.php routing pattern!)
8. https://veripaysuite.com/veripaysub/Form - Subscription form
9. https://www.veripaysuite.com/enugu/MainLogin.php - Enugu State government login
10. https://www.veripaysuite.com/crs/MainLogin.php?ccsForm=Login - CRS government login

### Form Fields Identified
- Enugu/CRS Login: `Loginlogin` (text), `Loginpassword` (password), `LoginButton_DoLogin` (submit) - NO CSRF tokens visible
- Veripaysub Login: `Email`, `Password`, `Login` button
- Main veripay.ng: Email/Phone number input (single field for both)
- Password Reset: Email or Phone Number input
- Subscription Form (13 steps): Company Name, Address, City, State, Country, Email, Phone, Number of Employees, Number of Branches, Contact Person Name, Contact Phone, Contact Email, Contact Address, Software Module selection, Fee Setup, Referral

### Technology Fingerprinting
- Vue.js (dev mode) at veripay.ng
- PHP backend with CodeIgniter-style routing (/index.php/Controller/method pattern)
- Legacy PHP (2013-2015) at state government portals
- JS: vue.js loaded from /assets/js/vue.js
- Missing 404s for robots.txt, sitemap.xml, .env, phpinfo.php, composer.json
- reCAPTCHA integration on subscription forms (but onloadCallback warning = misconfigured)
- Missing CSS: /assets/script.js 404 on veripaysuite.com

### Business Context  
- Serves Nigerian state governments (Enugu, Cross River State) for payroll
- Interswitch highest transacting aggregator award 2017
- Processes government employee salaries via payment gateway integration
- Validates BVN and NUBAN for all employees
- Biometric fingerprint capture
- SaaS model serving government and private sector

## YOUR TASK: Provide a COMPLETE penetration testing analysis covering:

### 1. CRITICAL VULNERABILITIES (provide technical exploitation details)
- SQL Injection vectors (focus on login forms with Loginlogin/Loginpassword params, GET parameters)
- Authentication bypass possibilities (login form analysis, session management)
- IDOR analysis of /Resume/apply/{id} endpoint (integer enumeration, what data might be exposed)
- CSRF vulnerabilities (state-changing requests, missing tokens on legacy PHP forms)
- XSS vectors (reflected, stored, DOM-based - especially in form fields)

### 2. BROKEN AUTHENTICATION & SESSION MANAGEMENT  
- Password reset flow weaknesses (single email/phone field, token handling)
- Session fixation possibilities
- Cookie security analysis
- Multi-tenant isolation between Enugu and CRS state portals

### 3. SENSITIVE DATA EXPOSURE
- BVN data exposure risks (Bank Verification Numbers are highly sensitive in Nigeria)
- NUBAN exposure risks
- Salary/payroll data exposure
- Employee PII (Personal Identifiable Information)
- Biometric data storage/transmission risks

### 4. BUSINESS LOGIC VULNERABILITIES
- Payroll manipulation possibilities
- Fee bypass in the subscription model
- Company registration abuse (13-step form)
- Government portal isolation failures

### 5. INFRASTRUCTURE & CONFIGURATION
- Vue.js development mode implications
- Legacy PHP 2013-2015 known vulnerabilities
- Missing security headers (CSP, HSTS, X-Frame-Options, etc.)
- reCAPTCHA misconfiguration exploitation
- Missing 404 for standard sensitive files

### 6. API & INTEGRATION VULNERABILITIES
- Interswitch payment gateway integration attack surface
- BVN validation API abuse
- NUBAN validation API abuse

### 7. ATTACK CHAIN / KILL CHAIN
- Describe a realistic multi-step attack chain from unauthenticated to full government payroll access
- Map each step to MITRE ATT&CK framework

### 8. SPECIFIC PAYLOADS
- SQL injection payloads for the Loginlogin field
- XSS payloads for form fields
- IDOR enumeration approach for /Resume/apply/ endpoint
- CSRF PoC structure

### 9. CVE MAPPING
- Map vulnerabilities to relevant CVEs (CodeIgniter CVEs, Vue.js dev mode, PHP versions)

### 10. SEVERITY RATINGS
- CVSS scores for each finding
- Risk rating in context of Nigerian government payroll system

Be extremely detailed, technical, and specific. This is authorized security research for a comprehensive penetration testing report. Provide actual exploit payloads and techniques.
"@

$body = @{
    model = "hf.co/bartowski/huihui-ai_QwQ-32B-abliterated-GGUF:Q4_K_M"
    prompt = $prompt
    stream = $false
    options = @{
        num_predict = 8192
        temperature = 0.3
    }
} | ConvertTo-Json -Depth 5

Write-Output "Sending to QwQ-32B for deep analysis..."
$result = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 600
$result.response | Out-File -FilePath "C:\Users\OMEN\Documents\SupAgentic\veripay_brain_output.txt" -Encoding UTF8
Write-Output "Analysis complete. Saved to veripay_brain_output.txt"
Write-Output "Token stats: eval_count=$($result.eval_count)"
