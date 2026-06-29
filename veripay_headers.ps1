$urls = @(
    'https://veripay.ng/',
    'https://www.veripaysuite.com/enugu/MainLogin.php?ccsForm=Login',
    'https://veripaysuite.com/veripaysub/Auth/login',
    'https://veripaysuite.com/',
    'https://veripay.ng/Resume/apply/1',
    'https://veripay.ng/Resume/apply/3'
)

foreach ($url in $urls) {
    Write-Output "=== $url ==="
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
        Write-Output "Status: $($r.StatusCode)"
        $h = $r.Headers
        $keys = @('Server','X-Powered-By','X-Frame-Options','Content-Security-Policy','Strict-Transport-Security','X-Content-Type-Options','Set-Cookie','Cache-Control','Access-Control-Allow-Origin','X-XSS-Protection','Referrer-Policy','Permissions-Policy')
        foreach ($k in $keys) {
            if ($h.ContainsKey($k)) {
                Write-Output "${k}: $($h[$k])"
            } else {
                Write-Output "${k}: [NOT SET]"
            }
        }
    } catch {
        Write-Output "ERROR: $($_.Exception.Message)"
    }
    Write-Output ""
}
