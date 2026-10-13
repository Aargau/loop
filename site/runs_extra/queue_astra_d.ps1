$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend openai --model gpt-6-astra --no-sampling --effort low --stop-on-cycle --min-interval 1 @argv --out "$base\$name" *> "$base\$name.log"
}
# BEFORE on Astra, 150 hops, 1024 budget (matches cb_json_prev_1024 and the causal-BEFORE run), 2026-09-06
Run "astra_json_prev" @("--init","json_prev","--steps","150","--max-tokens","1024")
"done" | Out-File "$base\queue_astra_d.done"
