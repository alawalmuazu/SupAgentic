#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

$toolsDir = "C:\Users\OMEN\Documents\SupAgentic\tools"

Write-Host "[*] Downloading Nuclei..." -ForegroundColor Cyan
$nucleiUrl = "https://github.com/projectdiscovery/nuclei/releases/download/v3.9.0/nuclei_3.9.0_windows_amd64.zip"
$nucleiZip = "$toolsDir\nuclei.zip"
Invoke-WebRequest -Uri $nucleiUrl -OutFile $nucleiZip

Write-Host "[*] Extracting Nuclei..." -ForegroundColor Cyan
Expand-Archive -Path $nucleiZip -DestinationPath "$toolsDir\nuclei_bin" -Force
Remove-Item $nucleiZip

Write-Host "[+] Nuclei provisioned successfully!" -ForegroundColor Green

Write-Host "[*] Downloading Caido CLI..." -ForegroundColor Cyan
# Using latest Caido CLI Windows release (v0.39.0 as an example, but downloading the zip directly)
$caidoUrl = "https://storage.googleapis.com/caido-releases/v0.39.0/caido-cli-v0.39.0-windows-x86_64.zip"
$caidoZip = "$toolsDir\caido.zip"
Invoke-WebRequest -Uri $caidoUrl -OutFile $caidoZip

Write-Host "[*] Extracting Caido..." -ForegroundColor Cyan
Expand-Archive -Path $caidoZip -DestinationPath "$toolsDir\caido_bin" -Force
Remove-Item $caidoZip

Write-Host "[+] Caido provisioned successfully!" -ForegroundColor Green
