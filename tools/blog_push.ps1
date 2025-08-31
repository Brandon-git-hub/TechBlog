Param(
  [string]$Message = "chore: update notes"
)
# Try run updater
if (Test-Path ".\update_index.py") {
  python .\update_index.py 2>$null
} elseif (Test-Path ".\tools\update_index.py") {
  python .\tools\update_index.py 2>$null
}
git add -A
# commit may fail if nothing changed
try {
  git commit -m $Message | Out-Null
} catch {
  Write-Host "Nothing to commit."
}
git push
Write-Host "✅ Pushed with message: $Message"
