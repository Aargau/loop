# Gemini as a third model family on the earlier experiments. Run from the repo root in a shell where
# $env:GEMINI_API_KEY is set. Starts seven detached processes:
#   four audience arms (40 hops), the two informed-loop arms (120 hops), and json_page (60 hops).
#   .\experiments\audience_20261016\queue_gemini.ps1 -Model <gemini model id> -Tag gemini
param([Parameter(Mandatory=$true)][string]$Model, [string]$Tag = "gemini", [string]$Effort = "low")
$D = "experiments/audience_20261016"
foreach ($arm in @("control","human","machine","self")) {
  Start-Process python -ArgumentList "loop.py --backend gemini --model $Model --init-file $D/inits/$arm.json --steps 40 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --out $D/runs/${Tag}_$arm" -NoNewWindow -RedirectStandardOutput "$D/runs/${Tag}_$arm.log" -RedirectStandardError "$D/runs/${Tag}_$arm.err"
}
foreach ($init in @("json_informed","json_informed_open")) {
  Start-Process python -ArgumentList "loop.py --backend gemini --model $Model --init $init --steps 120 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --max-chars 60000 --out runs/${Tag}_${init}_$Effort" -NoNewWindow -RedirectStandardOutput "runs/${Tag}_${init}_$Effort.log" -RedirectStandardError "runs/${Tag}_${init}_$Effort.err"
}
Start-Process python -ArgumentList "loop.py --backend gemini --model $Model --init json_page --steps 60 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --out runs/${Tag}_json_page_$Effort" -NoNewWindow -RedirectStandardOutput "runs/${Tag}_json_page_$Effort.log" -RedirectStandardError "runs/${Tag}_json_page_$Effort.err"
