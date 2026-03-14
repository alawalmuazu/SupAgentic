# ═══════════════════════════════════════════════════════════════
# SupAgentic — Tool Health Dashboard
# Checks git status, last commit date, and flags stale repos
# ═══════════════════════════════════════════════════════════════

$ToolsDir = Join-Path $PSScriptRoot "tools"
$StaleThresholdDays = 90

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║    SupAgentic — Tool Health Check     ║" -ForegroundColor Cyan
Write-Host "  ╚═══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$results = @()
$dirs = Get-ChildItem -Path $ToolsDir -Directory | Sort-Object Name

foreach ($dir in $dirs) {
    $gitDir = Join-Path $dir.FullName ".git"
    if (-not (Test-Path $gitDir)) {
        $results += [PSCustomObject]@{
            Name = $dir.Name; Status = "⚠️  No .git"; LastCommit = "N/A"; Age = "N/A"; Behind = "N/A"
        }
        continue
    }

    try {
        # Get last commit info
        $lastDate = git -C $dir.FullName log -1 --format="%ai" 2>&1
        $lastMsg  = git -C $dir.FullName log -1 --format="%s" 2>&1
        $commitDate = [datetime]::Parse($lastDate.Substring(0, 19))
        $daysAgo = [math]::Floor(((Get-Date) - $commitDate).TotalDays)

        # Check if behind remote
        $behind = "N/A"
        try {
            git -C $dir.FullName fetch --dry-run 2>&1 | Out-Null
            $behindCount = git -C $dir.FullName rev-list --count "HEAD..@{u}" 2>&1
            if ($behindCount -match '^\d+$') {
                $behind = if ([int]$behindCount -gt 0) { "$behindCount behind" } else { "Up to date" }
            }
        } catch { }

        # Status icon
        $statusIcon = if ($daysAgo -gt $StaleThresholdDays) { "🔴 Stale" }
                      elseif ($daysAgo -gt 30) { "🟡 Aging" }
                      else { "🟢 Fresh" }

        $results += [PSCustomObject]@{
            Name       = $dir.Name
            Status     = $statusIcon
            LastCommit = $commitDate.ToString("yyyy-MM-dd")
            Age        = "$daysAgo days"
            Behind     = $behind
        }
    } catch {
        $results += [PSCustomObject]@{
            Name = $dir.Name; Status = "❌ Error"; LastCommit = "N/A"; Age = "N/A"; Behind = "N/A"
        }
    }
}

# Display table
$results | Format-Table -AutoSize -Property Name, Status, LastCommit, Age, Behind

# Summary
$fresh = ($results | Where-Object { $_.Status -like "*Fresh*" }).Count
$aging = ($results | Where-Object { $_.Status -like "*Aging*" }).Count
$stale = ($results | Where-Object { $_.Status -like "*Stale*" }).Count

Write-Host ""
Write-Host "  Summary: 🟢 $fresh Fresh  |  🟡 $aging Aging  |  🔴 $stale Stale" -ForegroundColor White
Write-Host ""

# Offer to update stale repos
if ($stale -gt 0 -or $aging -gt 0) {
    $update = Read-Host "  Pull latest for all repos? (y/N)"
    if ($update -eq 'y' -or $update -eq 'Y') {
        foreach ($dir in $dirs) {
            Write-Host "  📥 Pulling $($dir.Name)..." -NoNewline
            try {
                git -C $dir.FullName pull --ff-only 2>&1 | Out-Null
                Write-Host " ✅" -ForegroundColor Green
            } catch {
                Write-Host " ❌" -ForegroundColor Red
            }
        }
    }
}
Write-Host ""
