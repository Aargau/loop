$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend cerebras @argv --out "$base\$name" *> "$base\$name.log"
}
# contemporaneous baselines for experiments/astra_causal_before_20260904: same budget (1024), same steps (300), same pacing
Run "cb_json_prev_1024" @("--init","json_prev","--steps","300","--max-tokens","1024","--stop-on-cycle","--min-interval","1")
"done" | Out-File "$base\queue_cb_ctrl.done"
