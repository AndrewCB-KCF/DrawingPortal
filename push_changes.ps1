param(
    [string]$Message = "Use SQLAlchemy engine for reads, fix Streamlit/AgGrid deprecation warnings"
)

$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

git add utils.py requirements.txt pages/1_Drawings.py pages/2_Revision_History.py pages/3_Approval_History.py pages/4_Certifications.py

$staged = git diff --cached --name-only
if (-not $staged) {
    Write-Host "No staged changes to commit."
    exit 0
}

Write-Host "Staged files:"
Write-Host $staged

git commit -m $Message
git push origin main

Write-Host "Pushed to origin/main."
