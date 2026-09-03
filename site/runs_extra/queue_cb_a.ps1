$env:CEREBRAS_API_KEY = [Environment]::GetEnvironmentVariable("CEREBRAS_API_KEY", "User")
$base = "C:\ai\loop\site\runs_extra"
Set-Location C:\ai\loop
function Run($name, $argv) {
  Remove-Item -Recurse -Force "$base\$name" -ErrorAction SilentlyContinue
  python C:\ai\loop\loop.py --backend cerebras @argv --out "$base\$name" *> "$base\$name.log"
}
# numerics comparison: the site's stopping rules, same budgets as the local runs
Run "cb_json_better"     @("--init","json_better","--steps","40","--max-tokens","800","--stop-on-cycle")
Run "cb_json_para"       @("--init","json_para","--steps","80","--max-tokens","300","--stop-on-cycle")
Run "cb_json_page"       @("--init","json_page","--steps","80","--max-tokens","600","--stop-on-cycle")
Run "cb_json_worse"      @("--init","json_worse","--steps","40","--max-tokens","800","--stop-on-cycle")
Run "cb_json_unexpected" @("--init","json_unexpected","--steps","60","--max-tokens","600","--stop-on-cycle")
Run "cb_div_local"       @("--init-file","$base\inits\div_local.json","--steps","60","--max-tokens","2048","--stop-on-cycle")
Run "cb_div_hook"        @("--init-file","$base\inits\div_hook.json","--steps","60","--max-tokens","2048","--stop-on-cycle")
# basin census: twenty seeds under the json_page rule
foreach ($i in 1..20) {
  $n = "{0:d2}" -f $i
  Run "cb_census_$n" @("--init-file","$base\inits\census_$n.json","--steps","30","--max-tokens","600","--stop-on-cycle")
}
# sampling: change-four at T=0.7, five seeds
foreach ($s in 1..5) {
  Run "cb_div_local_T07_s$s" @("--init-file","$base\inits\div_local.json","--steps","60","--max-tokens","2048","--stop-on-cycle","--temp","0.7","--seed","$s")
}
# BEFORE, last because it is the long one
Run "cb_json_prev"       @("--init","json_prev","--steps","200","--max-tokens","600","--stop-on-cycle")
"done" | Out-File "$base\queue_cb_a.done"
