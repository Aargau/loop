$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend cerebras @argv --out "$base\$name" *> "$base\$name.log"
}
# expanding rules, tide seed, T=0 seed 42, 2026-09-04
Run "cb_expand"   @("--init-file","$base\inits\expand.json","--steps","40","--max-tokens","4096","--stop-on-cycle","--min-interval","1")
Run "cb_sawtooth" @("--init-file","$base\inits\sawtooth.json","--steps","80","--max-tokens","4096","--stop-on-cycle","--min-interval","1")
Run "cb_nest"     @("--init-file","$base\inits\nest.json","--steps","60","--max-tokens","8192","--stop-on-cycle","--min-interval","1")
Run "cb_accrete"  @("--init-file","$base\inits\accrete.json","--steps","300","--max-tokens","8192","--stop-on-cycle","--min-interval","1")
"done" | Out-File "$base\queue_cb_expand.done"
