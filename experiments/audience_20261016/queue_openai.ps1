# Four audience arms on an OpenAI model through the API. Run from the repo root in a shell where $env:OPENAI_API_KEY is set.
#   .\experiments\audience_20261016\queue_openai.ps1 -Model gpt-6-astra -Tag astra
#   .\experiments\audience_20261016\queue_openai.ps1 -Model <gpt-6.1 id> -Tag gpt61
param([Parameter(Mandatory=$true)][string]$Model, [Parameter(Mandatory=$true)][string]$Tag, [string]$Effort = "low")
$D = "experiments/audience_20261016"
foreach ($arm in @("control","human","machine","self")) {
  Start-Process python -ArgumentList "loop.py --backend openai --model $Model --init-file $D/inits/$arm.json --steps 40 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --out $D/runs/${Tag}_$arm" -NoNewWindow -RedirectStandardOutput "$D/runs/${Tag}_$arm.log" -RedirectStandardError "$D/runs/${Tag}_$arm.err"
}
