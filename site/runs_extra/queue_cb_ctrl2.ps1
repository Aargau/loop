$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend cerebras @argv --out "$base\$name" *> "$base\$name.log"
}
Run "cb_json_next_1024" @("--init","json_next","--steps","300","--max-tokens","1024","--stop-on-cycle","--min-interval","1")
"done" | Out-File "$base\queue_cb_ctrl2.done"
