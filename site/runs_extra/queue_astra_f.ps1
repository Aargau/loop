$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend openai --model gpt-6-astra --no-sampling --effort low --stop-on-cycle --min-interval 1 @argv --out "$base\$name" *> "$base\$name.log"
}
# continuation of astra_json_prev_orig from its hop-150 output (overall hops 151..300), same settings, 2026-09-06
Run "astra_json_prev_orig_ext" @("--init-file","$base\inits\json_prev_orig_from_hop150.json","--steps","150","--max-tokens","1024")
"done" | Out-File "$base\queue_astra_f.done"
