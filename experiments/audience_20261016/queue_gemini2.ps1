# Argon on the relational rooms it asked about: BEFORE (json_prev, 150 hops, the Astra/Cerebras depth), the
# middle (json_mid, 60 hops), and the ledger room (site/runs_extra/inits/div_ledger.json, 100 hops, 8192
# tokens as in the Cerebras 300-hop run). Run from the repo root in the shell where $env:GEMINI_API_KEY is set.
#   .\experiments\audience_20261016\queue_gemini2.ps1 -Model gemini-4-argon -Tag gemini
param([Parameter(Mandatory=$true)][string]$Model, [string]$Tag = "gemini", [string]$Effort = "low")
Start-Process python -ArgumentList "loop.py --backend gemini --model $Model --init json_prev --steps 150 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --stop-on-cycle --out runs/${Tag}_json_prev_$Effort" -NoNewWindow -RedirectStandardOutput "runs/${Tag}_json_prev_$Effort.log" -RedirectStandardError "runs/${Tag}_json_prev_$Effort.err"
Start-Process python -ArgumentList "loop.py --backend gemini --model $Model --init json_mid --steps 60 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --out runs/${Tag}_json_mid_$Effort" -NoNewWindow -RedirectStandardOutput "runs/${Tag}_json_mid_$Effort.log" -RedirectStandardError "runs/${Tag}_json_mid_$Effort.err"
Start-Process python -ArgumentList "loop.py --backend gemini --model $Model --init-file site/runs_extra/inits/div_ledger.json --steps 100 --max-tokens 8192 --effort $Effort --no-sampling --min-interval 1 --out runs/${Tag}_div_ledger_$Effort" -NoNewWindow -RedirectStandardOutput "runs/${Tag}_div_ledger_$Effort.log" -RedirectStandardError "runs/${Tag}_div_ledger_$Effort.err"
