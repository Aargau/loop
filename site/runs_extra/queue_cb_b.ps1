$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend cerebras @argv --out "$base\$name" *> "$base\$name.log"
}
# ledger mechanism arms, 100 hops, 2048 tokens, no stop
Run "cb_div_ledger_nohook"  @("--init-file","$base\inits\div_ledger_nohook.json","--steps","100","--max-tokens","2048","--min-interval","2")
Run "cb_div_ledger_nostep"  @("--init-file","$base\inits\div_ledger_nostep.json","--steps","100","--max-tokens","2048","--min-interval","2")
Run "cb_div_ledger_control" @("--init-file","$base\inits\div_ledger_control.json","--steps","100","--max-tokens","2048","--min-interval","2")
# the diverse ledger to 300 hops at 8192 tokens (its first 100 hops double as the Cerebras baseline)
Run "cb_div_ledger_300"     @("--init-file","$base\inits\div_ledger.json","--steps","300","--max-tokens","8192","--min-interval","2")
"done" | Out-File "$base\queue_cb_b.done"
