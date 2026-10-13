$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend openai --model gpt-6-astra --no-sampling @argv --out "$base\$name" *> "$base\$name.log"
}
# smoke: 3 hops of json_page at low effort with a generous budget (does reasoning show in usage? cost per hop?)
Run "astra_smoke_low_4096"  @("--init","json_page","--steps","3","--max-tokens","4096","--effort","low","--min-interval","1")
# smoke: 2 hops at the site's usual 600 budget (does reasoning eat the visible passage?)
Run "astra_smoke_low_600"   @("--init","json_page","--steps","2","--max-tokens","600","--effort","low","--min-interval","1")
"done" | Out-File "$base\queue_astra_smoke.done"
