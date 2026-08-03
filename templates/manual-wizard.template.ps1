#requires -Version 7.0
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $false)]
    [string]$ManifestPath = (Join-Path $PSScriptRoot 'wizard.json'),

    [Parameter(Mandatory = $false)]
    [switch]$NonInteractive
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Write-Stage {
    param(
        [Parameter(Mandatory)]
        [int]$Index,
        [Parameter(Mandatory)]
        [int]$Total,
        [Parameter(Mandatory)]
        [string]$Title
    )

    Write-Host ''
    Write-Host ("[{0}/{1}] {2}" -f $Index, $Total, $Title)
}

function Open-ReviewedUrl {
    param([Parameter(Mandatory)][string]$Url)

    $uri = [Uri]$Url
    if ($uri.Scheme -notin @('http', 'https')) {
        throw "Unsupported URL scheme: $($uri.Scheme)"
    }
    Start-Process $uri.AbsoluteUri
}

function Read-PublicValue {
    param(
        [Parameter(Mandatory)][string]$Prompt,
        [Parameter(Mandatory)][string]$Name
    )

    $value = Read-Host $Prompt
    if ([string]::IsNullOrWhiteSpace($value)) {
        throw "$Name cannot be empty."
    }
    return $value
}

function Read-SecretValue {
    param(
        [Parameter(Mandatory)][string]$Prompt,
        [Parameter(Mandatory)][string]$Name
    )

    $value = Read-Host $Prompt -AsSecureString
    if ($value.Length -eq 0) {
        throw "$Name cannot be empty."
    }
    return $value
}

function Use-PlainTextSecret {
    param(
        [Parameter(Mandatory)][Security.SecureString]$Secret,
        [Parameter(Mandatory)][scriptblock]$Action
    )

    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secret)
    try {
        $plainText = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
        & $Action $plainText
    }
    finally {
        if ($null -ne $pointer) {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
        }
        Remove-Variable plainText -ErrorAction SilentlyContinue
    }
}

function Set-EnvValue {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Value
    )

    $resolved = [IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
    $directory = Split-Path -Parent $resolved
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }

    $escaped = $Value.Replace('`', '``').Replace('"', '`"')
    $line = '{0}="{1}"' -f $Name, $escaped
    $lines = if (Test-Path -LiteralPath $resolved) {
        @(Get-Content -LiteralPath $resolved)
    }
    else {
        @()
    }

    $pattern = '^{0}=' -f [Regex]::Escape($Name)
    $found = $false
    $updated = foreach ($existing in $lines) {
        if ($existing -match $pattern) {
            if (-not $found) {
                $found = $true
                $line
            }
        }
        else {
            $existing
        }
    }
    if (-not $found) {
        $updated += $line
    }

    [IO.File]::WriteAllLines($resolved, [string[]]$updated, [Text.UTF8Encoding]::new($false))
    Write-Host ("Updated {0} in {1}" -f $Name, $Path)
}

function Set-GitHubSecretValue {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][Security.SecureString]$Secret
    )

    Use-PlainTextSecret -Secret $Secret -Action {
        param([string]$Value)
        $Value | & gh secret set $Name --repo $Repository
        if ($LASTEXITCODE -ne 0) {
            throw "gh secret set failed for $Name."
        }
    }
    Write-Host ("GitHub Secret {0} is configured." -f $Name)
}

function Set-GitHubVariableValue {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Value
    )

    & gh variable set $Name --repo $Repository --body $Value
    if ($LASTEXITCODE -ne 0) {
        throw "gh variable set failed for $Name."
    }
    Write-Host ("GitHub Variable {0} is configured." -f $Name)
}

function Confirm-IrreversibleAction {
    param(
        [Parameter(Mandatory)][string]$Phrase,
        [Parameter(Mandatory)][string]$Rollback
    )

    if ($NonInteractive) {
        throw 'Irreversible actions cannot run with -NonInteractive.'
    }
    Write-Host ("Rollback: {0}" -f $Rollback)
    $answer = Read-Host ("Type exactly '{0}' to continue" -f $Phrase)
    if ($answer -cne $Phrase) {
        throw 'Confirmation phrase did not match. No irreversible command was run.'
    }
}

function Invoke-ReviewedCommand {
    param(
        [Parameter(Mandatory)][string]$Program,
        [Parameter(Mandatory)][string[]]$Arguments,
        [Parameter(Mandatory)][int[]]$ExpectedExitCodes
    )

    & $Program @Arguments
    if ($LASTEXITCODE -notin $ExpectedExitCodes) {
        throw ("{0} exited with code {1}." -f $Program, $LASTEXITCODE)
    }
}

if (-not (Test-Path -LiteralPath $ManifestPath)) {
    throw "Wizard manifest not found: $ManifestPath"
}

$manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json -Depth 20
$stages = @($manifest.stages)
if ($stages.Count -eq 0) {
    throw 'Wizard manifest contains no stages.'
}

Write-Host ("Starting: {0}" -f $manifest.title)
for ($index = 0; $index -lt $stages.Count; $index++) {
    $stage = $stages[$index]
    Write-Stage -Index ($index + 1) -Total $stages.Count -Title $stage.title

    switch ($stage.type) {
        'open_url' {
            Open-ReviewedUrl -Url $stage.url
        }
        'pause' {
            Start-Sleep -Seconds ([int]$stage.seconds)
        }
        'capture' {
            if ([bool]$stage.secret) {
                $secret = Read-SecretValue -Prompt $stage.prompt -Name $stage.name
                foreach ($destination in @($stage.destinations)) {
                    switch ($destination.type) {
                        'env' {
                            Use-PlainTextSecret -Secret $secret -Action {
                                param([string]$Value)
                                Set-EnvValue -Path $destination.path -Name $stage.name -Value $Value
                            }
                        }
                        'github_secret' {
                            Set-GitHubSecretValue -Repository $destination.repository -Name $stage.name -Secret $secret
                        }
                        'none' { }
                        default { throw "Unsupported secret destination: $($destination.type)" }
                    }
                }
                Remove-Variable secret -ErrorAction SilentlyContinue
            }
            else {
                $publicValue = Read-PublicValue -Prompt $stage.prompt -Name $stage.name
                foreach ($destination in @($stage.destinations)) {
                    switch ($destination.type) {
                        'env' {
                            Set-EnvValue -Path $destination.path -Name $stage.name -Value $publicValue
                        }
                        'github_variable' {
                            Set-GitHubVariableValue -Repository $destination.repository -Name $stage.name -Value $publicValue
                        }
                        'none' { }
                        default { throw "Unsupported public destination: $($destination.type)" }
                    }
                }
            }
        }
        'command' {
            if ([bool]$stage.irreversible) {
                Confirm-IrreversibleAction -Phrase $stage.confirmation_phrase -Rollback $stage.rollback
            }
            Invoke-ReviewedCommand `
                -Program $stage.program `
                -Arguments ([string[]]$stage.arguments) `
                -ExpectedExitCodes ([int[]]$stage.expected_exit_codes)
        }
        default {
            throw "Unsupported stage type: $($stage.type)"
        }
    }
}

Write-Host ''
Write-Host 'Wizard completed. Verify the non-secret success signals described in the human gate.'
