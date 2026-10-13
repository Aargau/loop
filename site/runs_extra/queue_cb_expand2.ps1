$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend cerebras @argv --out "$base\$name" *> "$base\$name.log"
}
# v2 wordings after the first pass froze at hop 2 (sawtooth read 300 as a cap) and hop 1 (nest quoted the rule back)
Run "cb_sawtooth2" @("--init-file","$base\inits\sawtooth2.json","--steps","80","--max-tokens","4096","--stop-on-cycle","--min-interval","1")
Run "cb_nest2"     @("--init-file","$base\inits\nest2.json","--steps","60","--max-tokens","8192","--stop-on-cycle","--min-interval","1")
"done" | Out-File "$base\queue_cb_expand2.done"
