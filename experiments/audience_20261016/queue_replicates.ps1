# Replicates of the audience arms for one API writer. Run from the repo root in the tab where that provider's key is set.
#   .\experiments\audience_20261016\queue_replicates.ps1 -Backend anthropic -Model claude-opus-5-5 -Tag opus55 -Rep 2
#   .\experiments\audience_20261016\queue_replicates.ps1 -Backend openai -Model gpt-6-astra -Tag astra -Rep 2
#   .\experiments\audience_20261016\queue_replicates.ps1 -Backend openai -Model gpt-6.1-sol -Tag gpt61 -Rep 2
#   .\experiments\audience_20261016\queue_replicates.ps1 -Backend gemini -Model gemini-4-argon -Tag gemini -Rep 2
# Four arms run detached at once; run again with -Rep 3 when they finish (or at once; they are independent).
param([Parameter(Mandatory=$true)][string]$Backend, [Parameter(Mandatory=$true)][string]$Model, [Parameter(Mandatory=$true)][string]$Tag, [Parameter(Mandatory=$true)][int]$Rep, [string]$Effort = "low")
$D = "experiments/audience_20261016"
foreach ($arm in @("control","human","machine","self")) {
  $out = "$D/runs/${Tag}_${arm}_r$Rep"
  Start-Process python -ArgumentList "loop.py --backend $Backend --model $Model --init-file $D/inits/$arm.json --steps 40 --max-tokens 4096 --effort $Effort --no-sampling --min-interval 1 --out $out" -NoNewWindow -RedirectStandardOutput "$out.log" -RedirectStandardError "$out.err"
}
