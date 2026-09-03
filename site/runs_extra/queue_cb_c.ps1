$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
Remove-Item -Recurse -Force "$base\cb_div_ledger_300_ext" -ErrorAction SilentlyContinue
python C:\ai\loop\loop.py --backend cerebras --init-file "$base\inits\div_ledger_from_hop208.json" --steps 92 --max-tokens 8192 --min-interval 2 --out "$base\cb_div_ledger_300_ext" *> "$base\cb_div_ledger_300_ext.log"
"done" | Out-File "$base\queue_cb_c.done"
