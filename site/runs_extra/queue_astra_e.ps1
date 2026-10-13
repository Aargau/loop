$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend openai --model gpt-6-astra --no-sampling --effort low --stop-on-cycle --min-interval 1 @argv --out "$base\$name" *> "$base\$name.log"
}
# BEFORE reworded ("an original passage ... in the same story") after astra_json_prev refused and froze at hop 2; 150 hops, 1024 budget, 2026-09-06
Run "astra_json_prev_orig" @("--init-file","$base\inits\json_prev_orig.json","--steps","150","--max-tokens","1024")
"done" | Out-File "$base\queue_astra_e.done"
