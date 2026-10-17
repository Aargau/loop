# Astra on the ten provenance inits, five replicates each, three hops. Run from the repo root in a shell where
# $env:OPENAI_API_KEY is set. 50 detached processes is too many at once; this runs them in five batches of ten.
$D = "experiments/provenance_20261017"
foreach ($rep in 1..5) {
  foreach ($init in Get-ChildItem "$D/inits/*.json") {
    $name = $init.BaseName
    python loop.py --backend openai --model gpt-6-astra --init-file $init.FullName --steps 3 --max-tokens 4096 --effort low --no-sampling --min-interval 0.5 --out "$D/runs/astra_${name}_r$rep" | Out-Null
    Write-Host "done astra_${name}_r$rep"
  }
}
