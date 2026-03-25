$repo = "cisco-ai-defense/defenseclaw"
$url = "https://api.github.com/repos/$repo"
$contentsUrl = "https://api.github.com/repos/$repo/contents"
$releaseDate = [datetime]"2026-03-27"
$today = Get-Date

Write-Host ""
Write-Host "  Cisco DefenseClaw Release Checker" -ForegroundColor Cyan
Write-Host "  ==================================" -ForegroundColor Cyan
Write-Host ""

if ($today.Date -lt $releaseDate.Date) {
    $daysLeft = ($releaseDate.Date - $today.Date).Days
    Write-Host "  [!] Not released yet. $daysLeft day(s) until March 27." -ForegroundColor Yellow
    Write-Host ""
    exit
}

try {
    $headers = @{ "User-Agent" = "SupAgentic" }
    $repoInfo = Invoke-RestMethod -Uri $url -Headers $headers -ErrorAction Stop
    $contents = Invoke-RestMethod -Uri $contentsUrl -Headers $headers -ErrorAction Stop

    $fileCount = ($contents | Where-Object { $_.type -eq "file" }).Count
    $dirCount  = ($contents | Where-Object { $_.type -eq "dir" }).Count

    Write-Host "  Repo:         $($repoInfo.full_name)" -ForegroundColor Green
    Write-Host "  Description:  $($repoInfo.description)"
    Write-Host "  Stars:        $($repoInfo.stargazers_count)"
    Write-Host "  Forks:        $($repoInfo.forks_count)"
    Write-Host "  Language:     $($repoInfo.language)"
    Write-Host "  Last Push:    $($repoInfo.pushed_at)"
    Write-Host "  Files:        $fileCount file(s), $dirCount dir(s) in root"
    Write-Host ""

    if ($fileCount -le 2 -and $dirCount -eq 0) {
        Write-Host "  [!] Still just LICENSE + README. No code dropped yet." -ForegroundColor Yellow
    } else {
        Write-Host "  [+] CODE IS LIVE! New files detected:" -ForegroundColor Green
        foreach ($item in $contents) {
            Write-Host "      $($item.type)  $($item.name)" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "  Clone: git clone https://github.com/$repo.git" -ForegroundColor Cyan
    }
    Write-Host ""
} catch {
    Write-Host "  [x] API error" -ForegroundColor Red
}
