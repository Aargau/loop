# Wait for the alternating run to finish (summary.json), then run the Qwen queue alone on the GPU.
$base = "C:\ai\loop\site\runs_extra"
while (-not (Test-Path "$base\alternating_json_page\summary.json")) { Start-Sleep -Seconds 30 }
Remove-Item -Recurse -Force "$base\qwen_json_mid" -ErrorAction SilentlyContinue
& "$base\queue.ps1"
