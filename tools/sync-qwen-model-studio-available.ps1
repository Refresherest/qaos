[CmdletBinding()]
param(
    [string]$SettingsPath = (Join-Path $PSScriptRoot "..\.qwen-sandbox\settings.json")
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $SettingsPath)) {
    throw "Qwen settings file was not found: $SettingsPath"
}

$candidateIds = @(
    "kimi-k2.7-code",
    "glm-5.1",
    "qwen3.7-max-preview",
    "qwen3.6-max-preview",
    "qwen3-32b",
    "deepseek-v3.2",
    "qwen3-coder-next",
    "qwen3-coder-plus-2025-09-23",
    "qwen-plus-latest",
    "qwen3-coder-480b-a35b-instruct",
    "qwen3-coder-30b-a3b-instruct",
    "qwen3-8b",
    "qwen3.6-27b",
    "qwen3-235b-a22b",
    "qwen-turbo",
    "qwen-mt-lite",
    "qwen3-next-80b-a3b-instruct",
    "qwen3.7-max-2026-05-17",
    "qwen3-30b-a3b",
    "qwen-mt-plus",
    "qwen3-14b",
    "qwen3-max-2025-09-23",
    "qwen-plus-character",
    "qwen3-coder-flash-2025-07-28",
    "qwen-flash-character",
    "qwen-plus-2025-04-28",
    "qwen-mt-turbo",
    "qwen3-30b-a3b-instruct-2507",
    "qwen-flash-2025-07-28",
    "qwen3.6-35b-a3b",
    "qwen-plus-2025-07-14",
    "qwen3-235b-a22b-instruct-2507",
    "qwq-plus",
    "qwen3-coder-plus-2025-07-22"
)

$settings = Get-Content -Raw -LiteralPath $SettingsPath | ConvertFrom-Json
if ($null -eq $settings.modelProviders) {
    $settings | Add-Member -NotePropertyName modelProviders -NotePropertyValue ([pscustomobject]@{})
}
if ($null -eq $settings.modelProviders.openai) {
    $settings.modelProviders | Add-Member -NotePropertyName openai -NotePropertyValue @()
}

$models = [System.Collections.Generic.List[object]]::new()
foreach ($model in @($settings.modelProviders.openai)) {
    $models.Add($model)
}

$existingIds = @{}
foreach ($model in $models) {
    $existingIds[$model.id] = $true
}

$added = [System.Collections.Generic.List[string]]::new()
foreach ($id in $candidateIds) {
    if ($existingIds.ContainsKey($id)) {
        continue
    }

    $models.Add([pscustomobject]@{
        id = $id
        name = "[QAOS quota-visible candidate] $id"
        description = "Visible with free quota in Model Studio on 2026-08-21; not yet endpoint-validated for QAOS agent work."
        envKey = "OPENAI_API_KEY"
        baseUrl = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    })
    $added.Add($id)
}

$settings.modelProviders.openai = @($models)
$settings | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $SettingsPath -Encoding utf8

[pscustomobject]@{
    settings_path = (Resolve-Path -LiteralPath $SettingsPath).Path
    added_count = $added.Count
    total_configured = @($settings.modelProviders.openai).Count
    added_model_ids = @($added)
} | ConvertTo-Json -Depth 4
