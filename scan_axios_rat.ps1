<#
.SYNOPSIS
Scans the current drive for the Axios Remote Access Trojan (RAT) payload spread
during the March 31, 2026 Claude Code npm v2.1.88 supply chain attack.

.DESCRIPTION
Searches for specific Indicators of Compromise (IOCs) across all package-lock.json, 
yarn.lock, and bun.lockb files in a specified directory or the entire filesystem.

IOCs:
- axios version 1.14.1
- axios version 0.30.4
- plain-crypto-js dependency

.EXAMPLE
./scan_axios_rat.ps1 -TargetDirectory "C:\Users\OMEN\Documents"
#>

param (
    [string]$TargetDirectory = $(Get-Location).Path
)

$ErrorActionPreference = "SilentlyContinue"

$IOCs = @(
    "axios`": `"1.14.1", 
    "axios`": `"0.30.4", 
    "plain-crypto-js"
)

$Lockfiles = @("package-lock.json", "yarn.lock", "bun.lockb")

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Red
Write-Host " SUPPLY CHAIN SCANNER: AXIOS RAT (Claude Code Leak)       " -ForegroundColor Yellow -BackgroundColor Black
Write-Host "==========================================================" -ForegroundColor Red
Write-Host "[*] Scanning Directory: $TargetDirectory"
Write-Host "[*] Target Files: $($Lockfiles -join ', ')"
Write-Host ""

$filesFound = 0
$detections = 0

foreach ($lockfile in $Lockfiles) {
    Write-Host "[~] Searching for $lockfile..." -ForegroundColor Cyan
    $files = Get-ChildItem -Path $TargetDirectory -Filter $lockfile -Recurse -File -Force
    
    foreach ($file in $files) {
        $filesFound++
        # Read the file content
        $content = Get-Content -Path $file.FullName -Raw
        
        foreach ($ioc in $IOCs) {
            if ($content -match $ioc) {
                Write-Host "     [!] RAT SIGNATURE DETECTED: $ioc" -ForegroundColor Red
                Write-Host "         Location: $($file.FullName)" -ForegroundColor Red
                $detections++
            }
        }
    }
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " SCAN COMPLETE" -ForegroundColor Cyan
Write-Host " Checked files : $filesFound"
Write-Host " Detections    : $detections"

if ($detections -gt 0) {
    Write-Host ""
    Write-Host "🚨 CRITICAL WARNING 🚨" -ForegroundColor White -BackgroundColor Red
    Write-Host "Your system has been compromised by the Axios RAT payload." -ForegroundColor Red
    Write-Host "- Disconnect from the internet immediately." -ForegroundColor Red
    Write-Host "- Rotate all secrets (API keys, passwords, tokens)." -ForegroundColor Red
    Write-Host "- Consider performing a clean OS reinstallation." -ForegroundColor Red
    Write-Host "==========================================================" -ForegroundColor Red
} else {
    Write-Host ""
    Write-Host "✅ SYSTEM CLEAN: No Axios RAT or plain-crypto-js IOCs found." -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
}
