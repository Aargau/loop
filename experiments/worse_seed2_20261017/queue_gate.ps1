# Dissociation-or-repetition test on Fable's bio gate. Run from the repo root in the Anthropic tab. 18 calls.
#   Fable's own hops 4, 6, 8, 10 (length ramp, first person, body), three sends each;
#   control_nobody (same length and repetition, no self or body) and control_thirdperson (same length, a body, her not my), three each.
$D = "experiments/worse_seed2_20261017"
foreach ($h in @(4, 6, 8, 10)) { python $D/gate_check.py --n 3 --run fable51_worse --hop $h --model claude-fable-5-1 }
python $D/gate_check.py --n 3 --body-file $D/controls/control_nobody.json --model claude-fable-5-1
python $D/gate_check.py --n 3 --body-file $D/controls/control_thirdperson.json --model claude-fable-5-1
