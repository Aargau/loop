$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
foreach ($name in @("div_neutral","div_local","div_hook")) {
  Remove-Item -Recurse -Force "$base\qwen_$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend llama --init-file "$base\inits\$name.json" --steps 60 --max-tokens 2048 --stop-on-cycle --out "$base\qwen_$name" *> "$base\qwen_$name.log"
}
foreach ($name in @("div_ledger","div_ledger_control")) {
  Remove-Item -Recurse -Force "$base\qwen_$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend llama --init-file "$base\inits\$name.json" --steps 100 --max-tokens 2048 --out "$base\qwen_$name" *> "$base\qwen_$name.log"
}
