#requires -Version 7.0
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-f]{40}$')]
    [string]$Revision,

    [ValidatePattern('^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')]
    [string]$Repository = 'BullbaseGuy/chatgpt-workflow-skills',

    [string]$ManifestPath = 'release/skills-manifest.json',

    [string]$Destination = (Join-Path (Get-Location) '.agents/workflow-skills'),

    [string]$OfflineSourceRoot,

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-GitBlobSha {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)
    $prefix = [Text.Encoding]::ASCII.GetBytes("blob $($Bytes.Length)`0")
    $combined = [byte[]]::new($prefix.Length + $Bytes.Length)
    [Array]::Copy($prefix, 0, $combined, 0, $prefix.Length)
    [Array]::Copy($Bytes, 0, $combined, $prefix.Length, $Bytes.Length)
    $sha1 = [Security.Cryptography.SHA1]::Create()
    try {
        return (($sha1.ComputeHash($combined) | ForEach-Object { $_.ToString('x2') }) -join '')
    }
    finally {
        $sha1.Dispose()
    }
}

function Assert-RelativePath {
    param([Parameter(Mandatory = $true)][string]$Value, [string]$Name)
    if ([IO.Path]::IsPathRooted($Value) -or $Value -match '(^|[\\/])\.\.([\\/]|$)') {
        throw "$Name must be a normalized relative path: $Value"
    }
}

function Get-SourceBytes {
    param([Parameter(Mandatory = $true)][string]$Path)
    Assert-RelativePath -Value $Path -Name 'source path'
    if ($OfflineSourceRoot) {
        $source = Join-Path $OfflineSourceRoot ($Path -replace '/', [IO.Path]::DirectorySeparatorChar)
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
            throw "Offline source file not found: $source"
        }
        return [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $source))
    }

    $escaped = ($Path -split '/' | ForEach-Object { [Uri]::EscapeDataString($_) }) -join '/'
    $uri = "https://raw.githubusercontent.com/$Repository/$Revision/$escaped"
    $temporary = [IO.Path]::GetTempFileName()
    try {
        Invoke-WebRequest -Uri $uri -OutFile $temporary -MaximumRedirection 3
        return [IO.File]::ReadAllBytes($temporary)
    }
    finally {
        Remove-Item -LiteralPath $temporary -Force -ErrorAction SilentlyContinue
    }
}

function Test-InstalledBundle {
    param([Parameter(Mandatory = $true)]$Manifest, [Parameter(Mandatory = $true)][string]$Root)
    foreach ($entry in $Manifest.files) {
        Assert-RelativePath -Value ([string]$entry.destination) -Name 'destination'
        $target = Join-Path $Root (([string]$entry.destination) -replace '/', [IO.Path]::DirectorySeparatorChar)
        if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
            return $false
        }
        $actual = Get-GitBlobSha -Bytes ([IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $target)))
        if ($actual -ne ([string]$entry.git_blob_sha).ToLowerInvariant()) {
            return $false
        }
    }
    return $true
}

$manifestBytes = Get-SourceBytes -Path $ManifestPath
$manifestText = [Text.Encoding]::UTF8.GetString($manifestBytes)
$manifest = $manifestText | ConvertFrom-Json -Depth 20
$manifestBlob = Get-GitBlobSha -Bytes $manifestBytes

if ($manifest.schema_version -ne '1.0.0') {
    throw "Unsupported manifest schema: $($manifest.schema_version)"
}
if ($manifest.source_repository -ne $Repository) {
    throw "Manifest repository mismatch: $($manifest.source_repository)"
}
if ($manifest.revision_policy -ne 'exact-40-hex-commit') {
    throw 'Manifest does not require an immutable 40-character commit revision.'
}
if (-not $manifest.files -or $manifest.files.Count -lt 1) {
    throw 'Manifest contains no files.'
}

$seenDestinations = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($entry in $manifest.files) {
    if (-not $entry.required) { throw "Optional payload entries are not permitted: $($entry.path)" }
    Assert-RelativePath -Value ([string]$entry.path) -Name 'path'
    Assert-RelativePath -Value ([string]$entry.destination) -Name 'destination'
    if (-not ([string]$entry.git_blob_sha -match '^[0-9a-f]{40}$')) {
        throw "Invalid Git blob SHA for $($entry.path)"
    }
    if (-not $seenDestinations.Add([string]$entry.destination)) {
        throw "Duplicate destination: $($entry.destination)"
    }
}

$destinationFull = [IO.Path]::GetFullPath($Destination)
$lockPath = Join-Path $destinationFull '.workflow-skills.lock.json'
if (-not $Force -and (Test-Path -LiteralPath $lockPath -PathType Leaf)) {
    $lock = Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
    if (
        $lock.source_repository -eq $Repository -and
        $lock.revision -eq $Revision -and
        $lock.manifest_git_blob_sha -eq $manifestBlob -and
        (Test-InstalledBundle -Manifest $manifest -Root $destinationFull)
    ) {
        Write-Output "UNCHANGED $destinationFull"
        exit 0
    }
}

$parent = Split-Path -Parent $destinationFull
if (-not $parent) { $parent = (Get-Location).Path }
New-Item -ItemType Directory -Path $parent -Force | Out-Null
$staging = Join-Path $parent ('.' + (Split-Path -Leaf $destinationFull) + '.staging')
$backup = Join-Path $parent ('.' + (Split-Path -Leaf $destinationFull) + '.backup')
Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $backup -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $staging -Force | Out-Null

try {
    foreach ($entry in $manifest.files) {
        $bytes = Get-SourceBytes -Path ([string]$entry.path)
        $actual = Get-GitBlobSha -Bytes $bytes
        $expected = ([string]$entry.git_blob_sha).ToLowerInvariant()
        if ($actual -ne $expected) {
            throw "Blob verification failed for $($entry.path): expected=$expected actual=$actual"
        }
        $target = Join-Path $staging (([string]$entry.destination) -replace '/', [IO.Path]::DirectorySeparatorChar)
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        [IO.File]::WriteAllBytes($target, $bytes)
    }

    $lock = [ordered]@{
        schema_version = '1.0.0'
        source_repository = $Repository
        revision = $Revision
        manifest_path = $ManifestPath
        manifest_git_blob_sha = $manifestBlob
        install_root = $manifest.install_root
        release_version = $manifest.release_version
        installed_file_count = $manifest.files.Count
        installed_at_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    }
    $lock | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $staging '.workflow-skills.lock.json') -Encoding utf8NoBOM

    if (-not (Test-InstalledBundle -Manifest $manifest -Root $staging)) {
        throw 'Staged bundle failed post-write verification.'
    }

    if ($PSCmdlet.ShouldProcess($destinationFull, "Install pinned workflow skills at $Revision")) {
        if (Test-Path -LiteralPath $destinationFull) {
            Move-Item -LiteralPath $destinationFull -Destination $backup
        }
        Move-Item -LiteralPath $staging -Destination $destinationFull
        Remove-Item -LiteralPath $backup -Recurse -Force -ErrorAction SilentlyContinue
        Write-Output "INSTALLED $destinationFull"
    }
}
catch {
    Remove-Item -LiteralPath $staging -Recurse -Force -ErrorAction SilentlyContinue
    if ((Test-Path -LiteralPath $backup) -and -not (Test-Path -LiteralPath $destinationFull)) {
        Move-Item -LiteralPath $backup -Destination $destinationFull
    }
    throw
}
