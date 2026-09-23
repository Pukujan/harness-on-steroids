$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$versionFile = Join-Path $PSScriptRoot 'opencode-version.txt'
$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    throw 'tools/opencode-version.txt must contain one semantic version.'
}

$installRoot = Join-Path $repoRoot '.tools\opencode'
$stageRoot = Join-Path $installRoot ".install-$PID"
$targetExe = Join-Path $installRoot 'opencode.exe'
$stageResolved = $null

New-Item -ItemType Directory -Path $installRoot -Force | Out-Null
New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
try {
    $stageResolved = (Resolve-Path -LiteralPath $stageRoot).Path
    $installResolved = (Resolve-Path -LiteralPath $installRoot).Path
    if (-not $stageResolved.StartsWith($installResolved + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Installer staging path escaped the repository-owned runtime directory.'
    }

    $headers = @{
        Accept = 'application/vnd.github+json'
        'User-Agent' = 'harness-on-steroids-opencode-bootstrap'
    }
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/anomalyco/opencode/releases/tags/v$version" -Headers $headers
    $asset = $release.assets | Where-Object name -eq 'opencode-windows-x64.zip' | Select-Object -First 1
    if ($null -eq $asset -or $asset.digest -notmatch '^sha256:[0-9a-fA-F]{64}$') {
        throw "The official v$version release has no verifiable Windows x64 asset digest."
    }
    $expectedDigest = $asset.digest.Substring(7).ToLowerInvariant()
    $archivePath = Join-Path $stageResolved 'opencode-windows-x64.zip'
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $archivePath
    $actualDigest = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualDigest -ne $expectedDigest) {
        throw 'The downloaded OpenCode release checksum did not match GitHub.'
    }

    $extractRoot = Join-Path $stageResolved 'unpacked'
    Expand-Archive -LiteralPath $archivePath -DestinationPath $extractRoot -Force
    $downloadedExe = Get-ChildItem -LiteralPath $extractRoot -Filter 'opencode.exe' -File -Recurse | Select-Object -First 1
    if ($null -eq $downloadedExe) {
        throw 'The verified release archive did not contain opencode.exe.'
    }
    $reportedVersion = (& $downloadedExe.FullName --version | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $reportedVersion -notmatch "(^|\s)v?$([regex]::Escape($version))($|\s)") {
        throw "Downloaded OpenCode reported an unexpected version: $reportedVersion"
    }

    $stagedExe = Join-Path $stageResolved 'opencode.exe'
    Copy-Item -LiteralPath $downloadedExe.FullName -Destination $stagedExe
    Move-Item -LiteralPath $stagedExe -Destination $targetExe -Force
    Write-Output "Installed verified OpenCode v$version at .tools/opencode/opencode.exe"
}
finally {
    if ($stageResolved -and (Test-Path -LiteralPath $stageResolved)) {
        $currentStage = (Resolve-Path -LiteralPath $stageResolved).Path
        $installResolved = (Resolve-Path -LiteralPath $installRoot).Path
        if ($currentStage.StartsWith($installResolved + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            Remove-Item -LiteralPath $currentStage -Recurse -Force
        }
    }
}
