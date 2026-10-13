$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend openai --model gpt-6-astra --no-sampling --effort low --steps 60 --stop-on-cycle --min-interval 1 @argv --out "$base\$name" *> "$base\$name.log"
}
# Astra light pass, 2026-09-06: low effort, provider-default sampling, budgets matched to the Qwen runs
Run "astra_sawtooth"  @("--init-file","$base\inits\sawtooth.json","--max-tokens","4096")
"done" | Out-File "$base\queue_astra_b.done"
