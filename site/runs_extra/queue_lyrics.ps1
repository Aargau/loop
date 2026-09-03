$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
foreach ($name in @("lyrics_next","lyrics_human_vague","lyrics_human_blacklist","lyrics_ai")) {
  Remove-Item -Recurse -Force "$base\qwen_$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend llama --init-file "$base\inits\$name.json" --steps 40 --max-tokens 600 --stop-on-cycle --out "$base\qwen_$name" *> "$base\qwen_$name.log"
}
