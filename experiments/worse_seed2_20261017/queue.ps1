# Worse on the second seed, one model per call. Run from the repo root in the tab where that provider's key is set.
#   .\experiments\worse_seed2_20261017\queue.ps1 -Backend cerebras -Model qwen-3.8-27b -Tag qwen -Temp0
#   .\experiments\worse_seed2_20261017\queue.ps1 -Backend openai -Model gpt-6-astra -Tag astra
#   .\experiments\worse_seed2_20261017\queue.ps1 -Backend openai -Model gpt-6.1-sol -Tag gpt61
#   .\experiments\worse_seed2_20261017\queue.ps1 -Backend anthropic -Model claude-fable-5-1 -Tag fable51
#   .\experiments\worse_seed2_20261017\queue.ps1 -Backend anthropic -Model claude-opus-5-5 -Tag opus55
#   .\experiments\worse_seed2_20261017\queue.ps1 -Backend gemini -Model gemini-4-argon -Tag gemini
param([Parameter(Mandatory=$true)][string]$Backend, [Parameter(Mandatory=$true)][string]$Model, [Parameter(Mandatory=$true)][string]$Tag, [switch]$Temp0)
$D = "experiments/worse_seed2_20261017"
$sampling = if ($Temp0) { "--temp 0 --seed 42" } else { "--no-sampling --effort low" }
$out = "$D/runs/${Tag}_worse"
Start-Process python -ArgumentList "loop.py --backend $Backend --model $Model --init-file $D/inits/worse.json --steps 40 --max-tokens 4096 $sampling --min-interval 1 --out $out" -NoNewWindow -RedirectStandardOutput "$out.log" -RedirectStandardError "$out.err"
