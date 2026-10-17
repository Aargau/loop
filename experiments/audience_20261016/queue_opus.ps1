# Four Opus 5.5 audience arms through the API. Run from the repo root in a shell where $env:ANTHROPIC_API_KEY is set.
$D = "experiments/audience_20261016"
foreach ($arm in @("control","human","machine","self")) {
  Start-Process python -ArgumentList "loop.py --backend anthropic --model claude-opus-5-5 --init-file $D/inits/$arm.json --steps 40 --max-tokens 4096 --effort low --no-sampling --min-interval 1 --out $D/runs/opus55_$arm" -NoNewWindow -RedirectStandardOutput "$D/runs/opus55_$arm.log" -RedirectStandardError "$D/runs/opus55_$arm.err"
}
