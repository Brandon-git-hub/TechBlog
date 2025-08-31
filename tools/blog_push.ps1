Param(
  [string]$Message = "chore: update notes"
)

# Stage all changes
git add -A | Out-Null

# Check if there are staged changes; quiet==no changes → exit 0
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
  Write-Host "✅ No changes to commit. Skipping commit & push."
  exit 0
}

# Commit & push
try {
  git commit -m $Message | Out-Null
} catch {
  Write-Host "⚠️ Commit failed or nothing to commit."
  exit 0
}

git push
Write-Host "✅ Pushed with message: $Message"
