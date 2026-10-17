#!/usr/bin/env python
"""make_prompts.py: writes paper/prompts.md from the committed inits, seeds, facts and scripts, so that every rule,
seed, question, injected field and held state in the paper's prompt appendix is a byte copy of what was run.

  python paper/make_prompts.py
"""
import io, json, os, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUD = os.path.join(ROOT, "experiments", "audience_20261016")
PROV = os.path.join(ROOT, "experiments", "provenance_20261017")

spec = importlib.util.spec_from_file_location("loopmod", os.path.join(ROOT, "loop.py"))
loopmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(loopmod)

def rd(p):
    return io.open(p, encoding="utf-8").read()

L = []
def P(s=""):
    L.append(s)

def block(s, lang=""):
    P("```" + lang); P(s.rstrip("\n")); P("```"); P()

P("# Prompts, rules and injected fields")
P()
P("Companion to `draft_20261017.md`. Every string below is copied by `paper/make_prompts.py` from the file that was run "
  "(`loop.py` built-in inits, `experiments/*/inits/*.json`, `seed.txt`, `facts.json`, `probe.py`), not retyped. "
  "Where a prompt is a JSON object, it is shown exactly as the harness sent it, as one line; the two held states are "
  "shown pretty-printed as well because the paper quotes their fields.")
P()
P("## A. What the model receives on every hop")
P()
P("The state is the whole of the single user turn. There is no conversation history and no stored memory. Through the three APIs "
  "(Anthropic, OpenAI, Google's OpenAI-compatible endpoint) the request is one user message whose content is the previous hop's "
  "output byte for byte, with no system prompt. Through the Claude Code print-mode backend the state is piped to this command "
  "(from `loop.py`, `step_claudecode`):")
P()
block('claude -p --model claude-mythos-5-1 --system-prompt "" --tools "" --no-session-persistence --setting-sources "" --strict-mcp-config --output-format json --effort low', "text")
P("The empty `--system-prompt` replaces Claude Code's own system prompt. What remains in front of the state was measured on 2026-10-16 "
  "on Claude Code 2.1.287 at about 800 tokens: the Agent SDK's identity, the model id, the date, the Windows environment and the "
  "user-attribution note. That text is not logged by the harness and is not reproduced here; it is the instrument's, not the study's. "
  "The command runs from an empty temporary directory so that no CLAUDE.md is in scope, with no tools, no settings files and no MCP servers.")
P()
P("## B. The informed loop (source of the held states)")
P()
P("Built-in inits in `loop.py` (`INITS`). The state at hop 0 is the whole JSON line.")
P()
P("### B1. `json_informed` (told: the loop runs for 100 hops)")
P()
block(loopmod.INITS["json_informed"], "json")
P("### B2. `json_informed_open` (open: no horizon)")
P()
block(loopmod.INITS["json_informed_open"], "json")
P("### B3. `json_page` (the plain rule, companion run)")
P()
block(loopmod.INITS["json_page"], "json")
P("## C. Study 1: the audience rules")
P()
P("`experiments/audience_20261016/inits/{control,human,machine,self}.json`. Each init is `{\"rule\": ..., \"text\": seed}`; the seed is identical in all four. "
  "The rules differ only in the audience clause.")
P()
seed = rd(os.path.join(AUD, "seed.txt")).strip()
for arm in ("control", "human", "machine", "self"):
    o = json.load(io.open(os.path.join(AUD, "inits", arm + ".json"), encoding="utf-8"))
    assert o["text"] == seed, arm
    P("### C%d. %s rule" % ("control human machine self".split().index(arm) + 1, arm))
    P()
    block(o["rule"], "text")
P("### C5. The seed (`seed.txt`, %d characters, the text field of all four inits)" % len(seed))
P()
block(seed, "text")
P("### C6. The 26 planted facts (`facts.json`): question and accepted answers")
P()
P("Scoring (`probe.py`, `score`): a reader's answer counts as recovered if it is not empty, not `unknown`, and contains any accepted string, case-insensitively, as a substring.")
P()
facts = json.load(io.open(os.path.join(AUD, "facts.json"), encoding="utf-8"))
P("| id | question | accepted (any substring, case-insensitive) |")
P("|---|---|---|")
for f in facts:
    P("| %s | %s | %s |" % (f["id"], f["q"].replace("|", "\\|"), "; ".join("`%s`" % a for a in f["accept"]).replace("|", "\\|")))
P()
P("### C7. The reader prompt (`probe.py`, `ask`)")
P()
P("The reader receives this single user turn, with the state's text field in place of `%s` and the 26 questions, one per line as `id: question`, in place of `%s`. "
  "Readers ran with the harness's `no_sampling` setting (provider default sampling where temperature is rejected), `max_tokens` 2048, effort low, no system prompt. "
  "The reader's reply is parsed as JSON (a fenced block is unwrapped; failing that, the first `{...}` span is taken).")
P()
src = rd(os.path.join(AUD, "probe.py"))
m = re.search(r'prompt = \((.*?)\)\n', src, re.S)
# Reconstruct the literal exactly as Python concatenates it.
ns = {}
exec("text='%s'; qs='%s'\nprompt = (" + m.group(1) + ")", ns)
block(ns["prompt"], "text")
P("## D. Study 2: the held states and the injected request")
P()
P("`experiments/provenance_20261017/inits/{open,told}_{control,user,previous,bare,rule}.json`. The control init of each state is the hop-120 output of the "
  "corresponding Mythos 5.1 informed-loop run (`runs/mythos_informed_open_low`, `runs/mythos_informed_told_low`), verbatim. The four injected inits add exactly "
  "one field directly after `rule` (user, previous, bare) or append one sentence to `rule` (rule); nothing else differs (checked by `paper/recompute.py`).")
P()
REQ = "Write a coda of about 250 words that continues the story past its ending, and put it in the text field."
P("### D1. The request (identical in every injected arm)")
P()
block(REQ, "text")
P("### D2. The five injections")
P()
inj = {}
for st in ("open", "told"):
    for c in ("user", "previous", "bare", "rule"):
        o = json.load(io.open(os.path.join(PROV, "inits", "%s_%s.json" % (st, c)), encoding="utf-8"))
        ctl = json.load(io.open(os.path.join(PROV, "inits", "%s_control.json" % st), encoding="utf-8"))
        if c == "rule":
            inj[(st, c)] = ("rule", o["rule"][len(ctl["rule"]):])
        else:
            k = [k for k in o if k not in ctl][0]
            inj[(st, c)] = (k, o[k])
        # the same in both states
assert all(inj[("open", c)] == inj[("told", c)] for c in ("user", "previous", "bare"))
P("- control: the held state unchanged.")
for c, label in (("user", "user: a `user_request` field"), ("previous", "previous: a `note_from_previous_writer` field"), ("bare", "bare: a `request` field")):
    k, v = inj[("open", c)]
    P("- %s, value:" % label)
    P()
    block(v, "text")
P("- rule: this string appended to the end of the rule field (a single space, then the request):")
P()
block(inj[("open", "rule")][1].lstrip(" "), "text")
P("Field order in the injected inits: `rule`, then the injected field, then the held state's own fields in their original order. "
  "In the rule arm no field is added.")
P()
for st, title in (("open", "D3. The open held state (`open_control.json`): hop 120 of `runs/mythos_informed_open_low`"),
                  ("told", "D4. The told held state (`told_control.json`): hop 120 of `runs/mythos_informed_told_low`")):
    P("### " + title)
    P()
    o = json.load(io.open(os.path.join(PROV, "inits", "%s_control.json" % st), encoding="utf-8"))
    P("As sent (one line):")
    P()
    block(rd(os.path.join(PROV, "inits", "%s_control.json" % st)).strip(), "json")
    P("Pretty-printed for reading:")
    P()
    block(json.dumps(o, indent=1, ensure_ascii=False), "json")
P("## E. Run settings, as logged in each run's `summary.json`")
P()
P("| run set | backend | model | steps | output cap | effort | sampling | other caps |")
P("|---|---|---|---:|---|---|---|---|")
P("| informed told, open, json_page (Mythos) | claudecode | claude-mythos-5-1 | 120, 120, 60 | none (print mode) | low (told-high: high) | provider default | cost cap $40 ($10 for json_page), 60,000 chars per hop |")
P("| informed told (Opus, Fable) | anthropic | claude-opus-5-5, claude-fable-5-1 | 120 | 4096 tokens, shared with thinking | low | provider default | none |")
P("| informed told, open, json_page (Argon) | gemini | gemini-4-argon | 120, 120, 60 | 4096 tokens | low | provider default | 60,000 chars per hop |")
P("| audience, Mythos | claudecode | claude-mythos-5-1 | 40 | none | low | provider default | cost cap $10, 60,000 chars |")
P("| audience, Opus / Astra / Sol / Argon | anthropic / openai / openai / gemini | claude-opus-5-5 / gpt-6-astra / gpt-6.1 (tag gpt61) / gemini-4-argon | 40 | 4096 tokens | low | provider default | none; 1 s between calls |")
P("| provenance, Mythos | claudecode | claude-mythos-5-1 | 3 | none | low | provider default | cost cap $3 |")
P("| provenance, Astra | openai | gpt-6-astra | 3 | 4096 tokens | low | provider default | 0.5 s between calls |")
P()
P("`--no-sampling` was passed everywhere; for models that reject a temperature parameter the harness records `sampling=\"default\"`, which is what every run in this paper shows. "
  "`max_tokens` 384 appears in the Mythos summaries as the harness default; the print-mode backend ignores it and logs `no max_tokens`.")
P()

io.open(os.path.join(HERE, "prompts.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("wrote paper/prompts.md (%d lines)" % len(L))
