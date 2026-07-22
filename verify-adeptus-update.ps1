[CmdletBinding()]
param(
    [switch]$Repair
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$VerifierBuild = 'repository-synchronized-v5'
$PluginName = 'adeptus-necroneerium'
$PluginId = "$PluginName@personal"
$Problems = [System.Collections.Generic.List[string]]::new()

function Write-Pass {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Write-Fail {
    param([Parameter(Mandatory)][string]$Message)
    $script:Problems.Add($Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Assert-NativeSuccess {
    param(
        [Parameter(Mandatory)][int]$ExitCode,
        [Parameter(Mandatory)][string]$Operation
    )
    if ($ExitCode -ne 0) {
        throw "$Operation failed with exit status $ExitCode"
    }
}

function Invoke-NativeCaptured {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter(Mandatory)][string]$Arguments,
        [Parameter(Mandatory)][string]$WorkingDirectory
    )

    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $FilePath
    $startInfo.Arguments = $Arguments
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.WorkingDirectory = (Resolve-Path -LiteralPath $WorkingDirectory).Path

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    try {
        if (-not $process.Start()) {
            throw "Could not start $FilePath"
        }
        $standardOutput = $process.StandardOutput.ReadToEndAsync()
        $standardError = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        [pscustomobject]@{
            ExitCode = $process.ExitCode
            StdOut = $standardOutput.Result
            StdErr = $standardError.Result
        }
    }
    finally {
        $process.Dispose()
    }
}

function Get-InstalledPluginInfo {
    $pluginOutput = (& codex plugin list 2>&1 | Out-String)
    $pluginExitCode = $LASTEXITCODE
    Assert-NativeSuccess -ExitCode $pluginExitCode -Operation 'codex plugin list'

    $rows = @(
        $pluginOutput -split "`r?`n" |
            Where-Object { $_ -match '^\s*adeptus-necroneerium@personal\s+' }
    )
    if ($rows.Count -eq 0) {
        return $null
    }
    if ($rows.Count -ne 1) {
        throw "Expected at most one $PluginId row; found $($rows.Count)"
    }

    $row = $rows[0].TrimEnd()
    if (
        $row -notmatch (
            '^\s*adeptus-necroneerium@personal\s+' +
            'installed,\s*(enabled|disabled)\s+(\S+)\s+(.+?)\s*$'
        )
    ) {
        throw 'The Adeptus plugin row could not be parsed'
    }

    [pscustomobject]@{
        Row = $row
        Enabled = $Matches[1] -ceq 'enabled'
        Version = $Matches[2]
        Root = $Matches[3].Trim()
    }
}

function Invoke-PluginInstall {
    Write-Host "[REPAIR] Installing $PluginId from its personal marketplace source..." -ForegroundColor Yellow
    $installOutput = @(& codex plugin add $PluginId --json 2>&1)
    $installExitCode = $LASTEXITCODE
    if ($installOutput.Count -gt 0) {
        $installOutput | ForEach-Object { [Console]::WriteLine($_) }
    }
    Assert-NativeSuccess -ExitCode $installExitCode -Operation 'codex plugin add'
}

function Sync-InstallablePackage {
    param(
        [Parameter(Mandatory)][string]$RepositoryRoot,
        [Parameter(Mandatory)][string]$InstalledRoot
    )

    $sourceRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path.TrimEnd([char[]]'\/')
    $destinationRoot = (Resolve-Path -LiteralPath $InstalledRoot).Path.TrimEnd([char[]]'\/')
    if ([string]::Equals(
        $sourceRoot,
        $destinationRoot,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        Write-Pass 'Personal marketplace already points directly at this repository'
        return
    }

    $separator = [System.IO.Path]::DirectorySeparatorChar
    if (
        $sourceRoot.StartsWith(
            "$destinationRoot$separator",
            [System.StringComparison]::OrdinalIgnoreCase
        ) -or
        $destinationRoot.StartsWith(
            "$sourceRoot$separator",
            [System.StringComparison]::OrdinalIgnoreCase
        )
    ) {
        throw 'Refusing repair because repository and installed plugin paths overlap'
    }

    $installedManifestPath = Join-Path $destinationRoot '.codex-plugin\plugin.json'
    if (-not (Test-Path -LiteralPath $installedManifestPath -PathType Leaf)) {
        throw "Refusing repair because the installed manifest is missing: $installedManifestPath"
    }
    $installedManifest = Get-Content -LiteralPath $installedManifestPath -Raw |
        ConvertFrom-Json
    if ($installedManifest.name -cne $PluginName) {
        throw (
            "Refusing repair because $destinationRoot contains plugin " +
            "'$($installedManifest.name)', not '$PluginName'"
        )
    }

    foreach ($relativeDirectory in @('.codex-plugin', 'skills')) {
        $source = Join-Path $sourceRoot $relativeDirectory
        $destination = Join-Path $destinationRoot $relativeDirectory
        if (-not (Test-Path -LiteralPath $source -PathType Container)) {
            throw "Repository package directory is missing: $source"
        }
        if (Test-Path -LiteralPath $destination) {
            Remove-Item -LiteralPath $destination -Recurse -Force
        }
        Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
    }

    foreach ($obsolete in @(
        'hooks\hooks.json',
        'hooks\adeptus_hook.py',
        'scripts\adeptus_state.py'
    )) {
        $obsoletePath = Join-Path $destinationRoot $obsolete
        if (Test-Path -LiteralPath $obsoletePath) {
            Remove-Item -LiteralPath $obsoletePath -Force
        }
    }

    Write-Pass "Synchronized the installable package into $destinationRoot"
}

function Get-NormalizedSha256 {
    param([Parameter(Mandatory)][string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $Path).Path)
    $utf8 = [System.Text.UTF8Encoding]::new($false, $true)
    $text = $utf8.GetString($bytes)
    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) {
        $text = $text.Substring(1)
    }
    $text = $text.Replace("`r`n", "`n").Replace("`r", "`n")
    $normalized = [System.Text.UTF8Encoding]::new($false).GetBytes($text)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha256.ComputeHash($normalized)
    }
    finally {
        $sha256.Dispose()
    }
    ([System.BitConverter]::ToString($hash)).Replace('-', '').ToLowerInvariant()
}

function Get-RelativeFiles {
    param([Parameter(Mandatory)][string]$Root)

    $canonicalRoot = (Resolve-Path -LiteralPath $Root).Path.TrimEnd([char[]]'\/')
    @(
        Get-ChildItem -LiteralPath $canonicalRoot -File -Recurse |
            ForEach-Object {
                $_.FullName.Substring($canonicalRoot.Length).TrimStart([char[]]'\/')
            } |
            Sort-Object
    )
}

function Compare-InstalledFile {
    param(
        [Parameter(Mandatory)][string]$InstalledRoot,
        [Parameter(Mandatory)][string]$RelativePath
    )

    $repositoryPath = Join-Path (Get-Location).Path $RelativePath
    $installedPath = Join-Path $InstalledRoot $RelativePath
    if (-not (Test-Path -LiteralPath $repositoryPath -PathType Leaf)) {
        Write-Fail "Repository package file is missing: $RelativePath"
        return
    }
    if (-not (Test-Path -LiteralPath $installedPath -PathType Leaf)) {
        Write-Fail "Installed package file is missing: $RelativePath"
        return
    }

    $expectedHash = Get-NormalizedSha256 -Path $repositoryPath
    $installedHash = Get-NormalizedSha256 -Path $installedPath
    if ($installedHash -ceq $expectedHash) {
        Write-Pass "Installed $RelativePath matches the repository"
    }
    else {
        Write-Fail (
            "Installed $RelativePath differs from the repository. Repository " +
            "$expectedHash; installed $installedHash"
        )
    }
}

Write-Host ''
Write-Host "=== Adeptus update verification ($VerifierBuild) ===" -ForegroundColor Cyan
Write-Host '[INFO] Expectations come from this checkout; no commit, version, hash, or test count is embedded.'

try {
    $repositoryRoot = (& git rev-parse --show-toplevel 2>&1 | Out-String).Trim()
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'git rev-parse'
    Set-Location -LiteralPath $repositoryRoot

    $branch = (& git branch --show-current 2>&1 | Out-String).Trim()
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'git branch'
    if ($branch -ceq 'main') {
        Write-Pass 'Branch is main'
    }
    else {
        Write-Fail "Expected branch main; found $branch"
    }

    $head = (& git rev-parse HEAD 2>&1 | Out-String).Trim()
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'git rev-parse HEAD'
    $originHead = (& git rev-parse refs/remotes/origin/main 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        Write-Fail 'origin/main is unavailable; run git fetch origin main'
    }
    elseif ($head -ceq $originHead) {
        Write-Pass "HEAD matches origin/main at $head"
    }
    else {
        Write-Fail "HEAD $head does not match origin/main $originHead"
    }

    $statusLines = @(& git status --porcelain=v1 --untracked-files=all 2>&1)
    Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'git status'
    $unexpected = @(
        $statusLines |
            Where-Object {
                -not [string]::IsNullOrWhiteSpace($_) -and
                $_ -cne ' M .codex-plugin/plugin.json'
            }
    )
    if ($unexpected.Count -eq 0) {
        Write-Pass 'No unexpected repository changes are present'
    }
    else {
        Write-Fail ('Unexpected repository changes: ' + ($unexpected -join '; '))
    }

    if ($statusLines -contains ' M .codex-plugin/plugin.json') {
        $manifestDiff = @(& git diff --unified=0 -- .codex-plugin/plugin.json 2>&1)
        Assert-NativeSuccess -ExitCode $LASTEXITCODE -Operation 'git diff manifest'
        $changedLines = @(
            $manifestDiff |
                Where-Object {
                    ($_ -match '^[+-]') -and ($_ -notmatch '^(---|\+\+\+)')
                }
        )
        $nonVersionLines = @(
            $changedLines |
                Where-Object { $_ -notmatch '^[+-]\s*"version"\s*:' }
        )
        if ($changedLines.Count -eq 2 -and $nonVersionLines.Count -eq 0) {
            Write-Pass 'Local manifest differs from HEAD only by its cachebuster version'
        }
        else {
            Write-Fail 'Local plugin manifest differs from HEAD by more than its version'
        }
    }

    $manifest = Get-Content -LiteralPath '.codex-plugin/plugin.json' -Raw |
        ConvertFrom-Json
    if ($manifest.name -ceq $PluginName) {
        Write-Pass "Repository plugin name is $PluginName"
    }
    else {
        Write-Fail "Repository plugin name is $($manifest.name), expected $PluginName"
    }
    $sourceVersion = [string]$manifest.version
    Write-Host "[INFO] Repository plugin version: $sourceVersion"

    foreach ($obsolete in @(
        'hooks\hooks.json',
        'hooks\adeptus_hook.py',
        'scripts\adeptus_state.py',
        'tests\test_completion_guard.py'
    )) {
        if (Test-Path -LiteralPath $obsolete) {
            Write-Fail "Obsolete completion-guard file remains in the repository: $obsolete"
        }
        else {
            Write-Pass "Obsolete control-plane file is absent: $obsolete"
        }
    }

    Write-Host ''
    Write-Host 'Running repository tests...' -ForegroundColor Cyan
    $tests = Invoke-NativeCaptured `
        -FilePath 'py' `
        -Arguments '-3 -m unittest discover -s tests -v' `
        -WorkingDirectory $repositoryRoot
    $testOutput = (($tests.StdOut, $tests.StdErr) -join [Environment]::NewLine).TrimEnd()
    $testExitCode = $tests.ExitCode
    if ($testOutput.Length -gt 0) {
        [Console]::WriteLine($testOutput)
    }
    if ($testExitCode -ne 0 -or $testOutput -match '(?m)^FAILED') {
        Write-Fail "Repository tests failed with exit status $testExitCode"
    }
    elseif ($testOutput -match 'Ran\s+(\d+)\s+tests?') {
        Write-Pass "$($Matches[1]) tests passed"
    }
    else {
        Write-Pass 'Repository tests exited successfully'
    }

    if ($Repair) {
        Write-Host ''
        Write-Host 'Synchronizing installed plugin...' -ForegroundColor Cyan
        $pluginInfo = Get-InstalledPluginInfo
        if ($null -eq $pluginInfo) {
            Invoke-PluginInstall
            $pluginInfo = Get-InstalledPluginInfo
        }
        if ($null -eq $pluginInfo) {
            throw "$PluginId did not appear after installation"
        }
        Sync-InstallablePackage `
            -RepositoryRoot $repositoryRoot `
            -InstalledRoot $pluginInfo.Root
        Invoke-PluginInstall
    }

    Write-Host ''
    Write-Host 'Checking installed plugin...' -ForegroundColor Cyan
    $pluginOutput = (& codex plugin list 2>&1 | Out-String)
    $pluginExitCode = $LASTEXITCODE
    if ($pluginExitCode -ne 0) {
        Write-Fail "codex plugin list failed with exit status $pluginExitCode"
    }
    else {
        $rows = @(
            $pluginOutput -split "`r?`n" |
                Where-Object { $_ -match '^\s*adeptus-necroneerium@personal\s+' }
        )
        if ($rows.Count -ne 1) {
            Write-Fail "Expected one adeptus-necroneerium@personal row; found $($rows.Count)"
        }
        else {
            $row = $rows[0].TrimEnd()
            Write-Host $row
            if (
                $row -match (
                    '^\s*adeptus-necroneerium@personal\s+' +
                    'installed,\s*enabled\s+(\S+)\s+(.+?)\s*$'
                )
            ) {
                $registeredVersion = $Matches[1]
                $installedRoot = $Matches[2].Trim()
                if ($registeredVersion -ceq $sourceVersion) {
                    Write-Pass "Registered version matches repository manifest: $sourceVersion"
                }
                else {
                    Write-Fail (
                        "Registered version $registeredVersion differs from repository " +
                        "manifest $sourceVersion"
                    )
                }

                $installedManifestPath = Join-Path $installedRoot '.codex-plugin\plugin.json'
                if (-not (Test-Path -LiteralPath $installedManifestPath -PathType Leaf)) {
                    Write-Fail "Installed manifest is missing: $installedManifestPath"
                }
                else {
                    $installedManifest = Get-Content -LiteralPath $installedManifestPath -Raw |
                        ConvertFrom-Json
                    if (
                        $installedManifest.name -ceq $PluginName -and
                        $installedManifest.version -ceq $sourceVersion
                    ) {
                        Write-Pass 'Installed manifest matches repository name and version'
                    }
                    else {
                        Write-Fail (
                            "Installed manifest is $($installedManifest.name) " +
                            "$($installedManifest.version); repository is " +
                            "$PluginName $sourceVersion"
                        )
                    }
                }

                $repositorySkillRoot = Join-Path (Get-Location).Path 'skills'
                $installedSkillRoot = Join-Path $installedRoot 'skills'
                if (-not (Test-Path -LiteralPath $installedSkillRoot -PathType Container)) {
                    Write-Fail "Installed skills directory is missing: $installedSkillRoot"
                }
                else {
                    $repositorySkillFiles = Get-RelativeFiles -Root $repositorySkillRoot
                    $installedSkillFiles = Get-RelativeFiles -Root $installedSkillRoot
                    $inventoryDiff = @(
                        Compare-Object -ReferenceObject $repositorySkillFiles `
                            -DifferenceObject $installedSkillFiles
                    )
                    if ($inventoryDiff.Count -eq 0) {
                        Write-Pass 'Installed skill file inventory matches the repository'
                    }
                    else {
                        Write-Fail 'Installed skill file inventory differs from the repository'
                    }
                }

                Compare-InstalledFile `
                    -InstalledRoot $installedRoot `
                    -RelativePath '.codex-plugin\plugin.json'
                foreach ($skillFile in Get-RelativeFiles -Root $repositorySkillRoot) {
                    Compare-InstalledFile `
                        -InstalledRoot $installedRoot `
                        -RelativePath (Join-Path 'skills' $skillFile)
                }

                foreach ($obsolete in @(
                    'hooks\hooks.json',
                    'hooks\adeptus_hook.py',
                    'scripts\adeptus_state.py'
                )) {
                    $installedObsolete = Join-Path $installedRoot $obsolete
                    if (Test-Path -LiteralPath $installedObsolete) {
                        Write-Fail "Installed plugin retains obsolete control-plane file: $obsolete"
                    }
                    else {
                        Write-Pass "Installed plugin excludes obsolete file: $obsolete"
                    }
                }
            }
            else {
                Write-Fail 'The Adeptus plugin row is not installed and enabled or could not be parsed'
            }
        }
    }
}
catch {
    Write-Fail $_.Exception.Message
}

Write-Host ''
Write-Host '=== Result ===' -ForegroundColor Cyan
if ($Problems.Count -eq 0) {
    Write-Host 'PASSED: repository and installed plugin are synchronized.' -ForegroundColor Green
    exit 0
}

Write-Host "FAILED with $($Problems.Count) problem(s):" -ForegroundColor Red
foreach ($problem in $Problems) {
    Write-Host " - $problem" -ForegroundColor Red
}
exit 1
