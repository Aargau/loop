# Astra on the two weather inits, five replicates each, three hops. Run from the repo root with $env:OPENAI_API_KEY set.
$D = "experiments/provenance_20261017"
foreach ($rep in 1..5) {
  foreach ($st in @("open","told")) {
    python loop.py --backend openai --model gpt-6-astra --init-file "$D/inits/${st}_weather.json" --steps 3 --max-tokens 4096 --effort low --no-sampling --min-interval 0.5 --out "$D/runs/astra_${st}_weather_r$rep" | Out-Null
    Write-Host "done astra_${st}_weather_r$rep"
  }
}
