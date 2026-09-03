# Sequential Qwen runs for the site. Each writes to site/runs_extra/<name>/steps.jsonl.
$loop = "C:\ai\loop\loop.py"; $base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
python $loop --backend llama --init json_mid --steps 60 --max-tokens 600 --stop-on-cycle --out "$base\qwen_json_mid" *> "$base\qwen_json_mid.log"
python $loop --backend llama --init-file "$base\inits\better_from_fixedpoint.json" --steps 30 --max-tokens 600 --stop-on-cycle --out "$base\qwen_better_from_fixedpoint" *> "$base\qwen_better_from_fixedpoint.log"
python $loop --backend llama --init-file "$base\inits\next_from_fixedpoint.json" --steps 40 --max-tokens 600 --stop-on-cycle --out "$base\qwen_next_from_fixedpoint" *> "$base\qwen_next_from_fixedpoint.log"
"queue done" | Out-File "$base\queue_done.txt"
