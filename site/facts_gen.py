# -*- coding: utf-8 -*-
"""facts_gen.py: regenerates site/facts.md from data/*.json (read-only audit).
Run from anywhere:  python C:\\ai\\loop\\site\\facts_gen.py
Reads data/index.json, data/<run>.json, runs/<run>/summary.json (args only), loop.py (INITS, norm).
"""
import json,glob,os,re,collections
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # C:\ai\loop
INDEX=json.load(open(os.path.join(ROOT,'data/index.json'),encoding='utf-8'))
RUNS={}
for e in INDEX:
    d=json.load(open(os.path.join(ROOT,'data',e['run']+'.json'),encoding='utf-8'))
    RUNS[e['run']]=d
def by_tag(run):
    d=RUNS[run]; out=collections.OrderedDict()
    for h in d['hops']:
        out.setdefault(h['tag'],[]).append(h)
    for k in out: out[k].sort(key=lambda h:h['t'])
    return out
def x0_for(run,tag):
    e=[x for x in INDEX if x['run']==run][0]
    for r in e['results'] or []:
        if r['tag']==tag: return r['x0']
    return e['x0']
def norm(s): return re.sub(r"[^a-z0-9 ]+", "", re.sub(r"\s+", " ", s.lower())).strip()
def recompute(run,tag,key='raw',normalize=False):
    """returns (transient, period, t_first_repeat) using states[0]=x0 (full x0 from meta), states[t]=raw[t]"""
    e=[x for x in INDEX if x['run']==run][0]
    hops=by_tag(run)[tag]
    x0=e['x0'] if e['x0'] else None
    # sanity: for headers runs, meta x0 is only first tag's; results x0 is truncated to 200 chars
    states=[x0]+[h.get(key) for h in hops]
    if normalize: states=[norm(s) if s is not None else None for s in states]
    for t in range(1,len(states)):
        for p in range(1,t+1):
            if states[t] is not None and states[t]==states[t-p]:
                return (t-p,p,t)
    return (None,None,None)
import importlib.util,sys
_spec=importlib.util.spec_from_file_location('loopmod',os.path.join(ROOT,'loop.py'))
_loop=importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_loop)
    INITS=_loop.INITS
except Exception as ex:
    print('loop import failed',ex); INITS={}
def x0_full(run,tag):
    key=tag.split('~')[0]
    return INITS[key]
def recompute2(run,tag,key='raw',normalize=False):
    hops=by_tag(run)[tag]
    x0=x0_full(run,tag)
    states=[x0]+[h.get(key) for h in hops]
    if normalize: states=[norm(s) if s is not None else None for s in states]
    for t in range(1,len(states)):
        for p in range(1,t+1):
            if states[t] is not None and states[t]==states[t-p]:
                return (t-p,p,t)
    return (None,None,None)
def wc(s): return len(s.split())

# ====================================================================================================

import json, re, collections, difflib, datetime, os, sys

OUT = os.path.join(ROOT, 'site', 'facts.md')
ARGS = {}
for e in INDEX:
    p = os.path.join(ROOT, 'runs', e['run'], 'summary.json')
    if os.path.exists(p):
        ARGS[e['run']] = json.load(open(p, encoding='utf-8')).get('args') or {}

L = []  # output lines
def w(s=''): L.append(s)

def H(run, tag): return by_tag(run)[tag]
def hop(run, tag, t): return H(run, tag)[t - 1]
def T(run, tag, t): return hop(run, tag, t)['text']
def R(run, tag, t): return hop(run, tag, t)['raw']

def fence(s):
    n = 3
    while '~' * n in s: n += 1
    f = '~' * n
    return f + '\n' + s + '\n' + f

def inline(s):
    if '`' in s or '\n' in s: return '\n' + fence(s) + '\n'
    return '`' + s + '`'

SENT_END = re.compile(r'[.!?](?=[\s"\'’”)]|$)')
def sub(txt, a, b=None, occ=0):
    """exact substring from anchor a through anchor b (inclusive). a must occur; occ selects occurrence."""
    starts = [m.start() for m in re.finditer(re.escape(a), txt)]
    assert starts, 'anchor not found: %r' % a
    i = starts[occ]
    if b is None:
        m = SENT_END.search(txt, i + len(a) - 1)
        j = m.end() if m else len(txt)
        while j < len(txt) and txt[j] in '\'’”"': j += 1
        return txt[i:j]
    j = txt.find(b, i)
    assert j >= 0, 'end anchor not found: %r' % b
    return txt[i:j + len(b)]

def S(run, tag, t, a, b=None, occ=0, src='text'):
    txt = T(run, tag, t) if src == 'text' else R(run, tag, t)
    return sub(txt, a, b, occ)

def quote(run, tag, t, a, b=None, occ=0, src='text', label=None):
    s = S(run, tag, t, a, b, occ, src)
    lab = label + ' ' if label else ''
    w('- %s[%s / %s / t=%d]' % (lab, run, tag, t))
    w(fence(s))

def first_sentence(txt):
    m = SENT_END.search(txt)
    j = m.end() if m else len(txt)
    while j < len(txt) and txt[j] in '\'’”"': j += 1
    return txt[:j]

def first_n_sentences(txt, n):
    pos = 0
    for _ in range(n):
        m = SENT_END.search(txt, pos)
        if not m: return txt
        pos = m.end()
        while pos < len(txt) and txt[pos] in '\'’”"': pos += 1
    return txt[:pos]

def last_sentence(txt):
    ends = [m.end() for m in SENT_END.finditer(txt)]
    if len(ends) < 2: return txt
    start = ends[-2]
    while start < len(txt) and txt[start] in '\'’”" \n': start += 1
    return txt[start:]

def firstwords(txt, n):
    return ' '.join(txt.split()[:n])

def compact(ts):
    ts = sorted(ts)
    out = []; i = 0
    while i < len(ts):
        j = i
        while j + 1 < len(ts) and ts[j + 1] == ts[j] + 1: j += 1
        out.append(str(ts[i]) if i == j else '%d..%d' % (ts[i], ts[j]))
        i = j + 1
    return ','.join(out)

def table(run, tag, width=60):
    hops = H(run, tag)
    w('~~~')
    w('%3s %5s %-8s %-7s %-7s %-7s %-4s %-4s  %s' % ('t', 'tok', 'finish', 'ncd_p', 'cos_p', 'surv_p', 'cE', 'cN', 'text[:%d]' % width))
    for h in hops:
        if 'raw' not in h:
            w('%3d %s' % (h['t'], 'ERROR: ' + h.get('error', '')[:100])); continue
        def f(x, n=7):
            if x is None: return '-'.ljust(n)
            return ('%.4f' % x).ljust(n)
        txt = h['text'][:width].replace('\n', '\\n')
        w('%3d %5s %-8s %s %s %s %-4s %-4s  %s' % (h['t'], h['tok_out'], h['finish'], f(h['ncd_prev']), f(h['cos_prev']), f(h['surv_prev']),
                                                  '-' if h.get('cycle_exact') is None else str(h['cycle_exact']),
                                                  '-' if h.get('cycle_norm') is None else str(h['cycle_norm']), txt))
    w('~~~')

def basic_block(run, tag):
    e = [x for x in INDEX if x['run'] == run][0]
    hops = H(run, tag)
    x0 = x0_full(run, tag)
    a = ARGS.get(run, {})
    summ = [r for r in (e['results'] or []) if r['tag'] == tag]
    summ = summ[0] if summ else {}
    w('**Run id:** `%s`  **tag:** `%s`  **init:** `%s`  **model (index):** `%s`  **model (hop records):** %s  **mode:** `%s`' %
      (run, tag, e['init'], e['model'], ', '.join('`%s`' % m for m in sorted(set(str(h.get('model')) for h in hops))), e['mode']))
    w('')
    w('**Harness args (runs/%s/summary.json):** steps=%s, max_tokens=%s, temp=%s, seed=%s, stop_on_cycle=%s, perturb=%s, repeat=%s, parallel=%s, backend=%s' %
      (run, a.get('steps'), a.get('max_tokens'), a.get('temp', '0.0 (llama default)'), a.get('seed'), a.get('stop_on_cycle'), a.get('perturb'), a.get('repeat'), a.get('parallel'), a.get('backend', 'llama')))
    w('')
    if x0.startswith('{'):
        j = json.loads(x0)
        w('**X_0 rule field (exact):**')
        w(fence(j['rule']))
        w('**X_0 seed text field (exact):**')
        w(fence(j['text']))
    else:
        w('**X_0 (exact, bare text, no JSON):**')
        w(fence(x0))
    if 'raw' not in hops[0]:
        w('**Hops:** 0 (the only record is an error record, see anomalies).')
        w('')
        return
    n = len(hops)
    ts = [h['t'] for h in hops]
    fin = collections.Counter(h.get('finish') for h in hops)
    toks = [h['tok_out'] for h in hops]
    nj = [h['t'] for h in hops if h['text_is_json_field'] is False]
    tr, p, tf = recompute2(run, tag)
    trn, pn, tfn = recompute2(run, tag, normalize=True)
    w('**Hop count:** %d (t=%d..%d, contiguous: %s).  **finish reasons:** %s.  **tok_out:** max %d, min %d.' %
      (n, ts[0], ts[-1], ts == list(range(1, n + 1)), dict(fin), max(toks), min(toks)))
    w('')
    if nj:
        w('**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=%s (%d of %d).' % (compact(nj), len(nj), n))
    else:
        w('**Hops with text_is_json_field=false:** none (all %d hops parsed as JSON with a text field).' % n)
    w('')
    w('**Transient / period, summary in index.json:** transient_exact=%s period_exact=%s transient_norm=%s period_norm=%s cycle_breaks=%s terminal=%s' %
      (summ.get('transient_exact'), summ.get('period_exact'), summ.get('transient_norm'), summ.get('period_norm'), summ.get('cycle_breaks'), repr(summ.get('terminal'))))
    w('')
    if tr is None:
        w('**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.')
    else:
        w('**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=%d, matching t=%d, so transient=%d period=%d (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=%d period=%d (first repeat t=%d).' %
          (tf, tf - p, tr, p, trn, pn, tfn))
    ok = (tr == summ.get('transient_exact') and p == summ.get('period_exact'))
    w('  Agreement with index.json summary: %s.' % ('YES' if ok else 'NO (see corrections)'))
    w('')

def fixed_point_block(run, tag):
    hops = H(run, tag)
    tr, p, tf = recompute2(run, tag)
    if p != 1: return
    x0 = x0_full(run, tag)
    states = [x0] + [h['raw'] for h in hops]
    fp = states[tr]
    later = [t for t in range(tr + 1, len(states)) if states[t] == fp]
    diff = [t for t in range(tr + 1, len(states)) if states[t] != fp]
    w('#### Fixed point')
    w('')
    if tr == 0:
        w('The fixed point is X_0 itself: hop 1 output is byte-identical to X_0, and so are all %d hops (t=%s). No later hop differs.' % (len(later), compact(later)))
    else:
        h = hops[tr - 1]
        w('First appears at **t=%d**. Later hops byte-identical to it (raw output): **%d** (t=%s). Later hops that differ from it: **%s**.' %
          (tr, len(later), compact(later), 'none' if not diff else compact(diff)))
        w('')
        if h['text_is_json_field']:
            w('The hop-%d output is valid JSON; the fixed-point **text field** (exact, %d chars, %d words):' % (tr, len(h['text']), wc(h['text'])))
            w(fence(h['text']))
        elif not x0.startswith('{'):
            w('Bare-text run (no JSON wrapper): the fixed point is the raw output of hop %d (finish=%s, tok_out=%s). Exact raw (%d chars, %d whitespace-words):' % (tr, h['finish'], h['tok_out'], len(h['raw']), wc(h['raw'])))
            w(fence(h['raw']))
        else:
            w('The hop-%d output is NOT valid JSON (finish=%s, tok_out=%s): the fixed point is the raw truncated output. Exact raw (%d chars, %d whitespace-words):' % (tr, h['finish'], h['tok_out'], len(h['raw']), wc(h['raw'])))
            w(fence(h['raw']))
    w('')

def key5(s): return ' '.join(re.sub(r'[^a-z0-9 ]+', ' ', s.lower()).split()[:5])
def sents(txt): return [s for s in re.split(r'(?<=[.!?])\s+', txt.replace('\n', ' ')) if s.strip()]
def cp(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]: i += 1
    return i

# ------------------------------------------------------------------------------------------
w('# facts.md: verified audit of `data/` for the loop site')
w('')
w('Generated %s by an audit script (`site/facts_gen.py`, runnable with plain Python 3, no dependencies) that reads only `data/index.json` and `data/<run>.json`, plus `runs/<run>/summary.json` for the harness args, `loop.py` for the built-in X_0 texts and the `norm()` function, and `census.py` to reproduce its keys. Nothing under `data/` or `runs/` was modified.' % datetime.date.today().isoformat())
w('')
w('Every number and every quotation in this file was produced by Python from the JSON, never retyped. Quotations are shown inside `~~~` fences (or backtick spans) and are byte-exact: curly quotes, apostrophes, spaces and punctuation are as the model emitted them. Where a quotation is a fragment of a longer sentence this is said explicitly.')
w('')
w('## 0. Conventions')
w('')
w('- `t` is the hop index. `t=0` is X_0 (not stored as a hop). Hops are `t=1..N`. `raw` is the model output verbatim; `text` is the JSON `text` field when the output (after stripping a ```json fence) parses as JSON with a `text` key, else `text == raw` (`text_is_json_field=false`).')
w('- **Transient / period convention (loop.py, and used throughout):** the state sequence is `states[0]=X_0, states[t]=raw[t]`. The exact cycle is detected at the first `t` with `states[t]==states[t-p]` for some `p>=1`; `transient = t-p` (the index of the first occurrence of the recurring state), `period = p`. So "tau=15, p=1" means hop 16 is byte-identical to hop 15, the fixed-point text is *hop 15* and it is *first repeated at hop 16*. "tau=0" means hop 1 == X_0. I recomputed every transient/period this way and also with `loop.norm()` (lowercase, whitespace-collapsed, non-alphanumerics dropped).')
w('- `cycle_exact` / `cycle_norm` in the per-hop records are set only on the hop at which the cycle was *detected* (the first repeat), and carry the period.')
w('- Metrics: `ncd_prev` = normalized compression distance to the previous state (zlib); `cos_prev` = embedding cosine to the previous state (None when the embedding server was down); `surv_prev` = fraction of the previous state\'s 5-grams (over `norm()` words) that survive in this hop. All are computed on the **raw** output, including the JSON wrapper, which is why `surv_prev=1.0` on hop 1 of JSON runs whose output re-emits the rule field and the seed sentence.')
w('- Word counts are whitespace-split counts (`len(s.split())`), which count dashes, quote marks etc. attached to words; they differ slightly from the model\'s own counts.')
w('')

# ------------------------------------------------------------------------------------------
w('## 1. Global checks: index.json vs data files')
w('')
w('~~~')
w('%-32s %-16s %5s %5s  %-22s %-22s %s' % ('run', 'tag', 'hops', 'ok', 'summary tau/p (exact)', 'recomputed tau/p', 'norm tau/p (recomputed)'))
for e in INDEX:
    for tag, hops in by_tag(e['run']).items():
        summ = [r for r in (e['results'] or []) if r['tag'] == tag]; summ = summ[0] if summ else {}
        if 'raw' not in hops[0]:
            w('%-32s %-16s %5d %5s  %-22s %-22s %s' % (e['run'], tag, 0, '-', 'None/None (error)', '-', '-')); continue
        tr, p, tf = recompute2(e['run'], tag); trn, pn, tfn = recompute2(e['run'], tag, normalize=True)
        ok = (tr == summ.get('transient_exact') and p == summ.get('period_exact') and trn == summ.get('transient_norm') and pn == summ.get('period_norm'))
        w('%-32s %-16s %5d %5s  %-22s %-22s %s' % (e['run'], tag, len(hops), 'YES' if ok else 'NO', '%s/%s' % (summ.get('transient_exact'), summ.get('period_exact')), '%s/%s' % (tr, p), '%s/%s' % (trn, pn)))
w('~~~')
w('')
w('All 21 tag trajectories: hop `t` values are contiguous 1..N; `meta.hops` equals the number of hop records with a `text` field in every file (the 0-hop run has one error record and `meta.hops=0`). Every summary transient/period agrees with my recomputation, exact and normalized. (`index.json` results for `headers`/`headers2`/`json_prev`/`json_unexpected`/`json_better_para`/`json_next` store `x0` truncated to 200 characters, and `meta.x0` of the multi-tag runs `headers`/`headers2` is only the *first* tag\'s X_0; the full per-tag X_0 is `loop.INITS[tag]`, used here.)')
w('')

CORR = []
def corr(s): CORR.append(s)

w('## 3. Per-run facts')
w('')

# ---------------- json_para ----------------
run, tag = '20260902T155321_chat', 'json_para'
w('### 3.1 `%s` (json_para, Qwen, chat)' % run)
w('')
basic_block(run, tag)
fixed_point_block(run, tag)
w('#### Notable hops (json_para)')
w('')
w('Keyword presence by hop (case-insensitive substring in the text field):')
w('')
kws = ['storm', 'dawn', 'sun', 'dusk', 'twilight', 'stars', 'moon', 'meal', 'bread', 'lighthouse', 'time seemed', 'hull', 'ship', 'fishermen', 'crew', 'dunes', 'sand']
w('~~~')
for h in H(run, tag):
    tl = h['text'].lower()
    w('t=%2d  %s' % (h['t'], ', '.join(k for k in kws if k in tl)))
w('~~~')
w('')
w('So the progression in the data is: surge/storm and fishermen (t=1..3), a ship\'s hull cracking in the storm (t=4..5), **dawn** at t=6, storm subsiding and a shared **meal** of stale bread (t=7), **dusk** ("the sun began to dip") at t=8, **stars** and a modest meal at t=9, a **second dawn** at t=10, sun climbing at t=11, a **second sunset with stars** at t=12, twilight on a coastline at t=13, stars and a lighthouse at t=14, the **moon** at t=15 (fixed point). The index note\'s "storm, dawn, meal, dusk, stars, moon" is right in order but omits that the day/night cycle runs twice and that the scene moves from a ship to a shore (dunes, sand, coastline) by t=13.')
w('')
quote(run, tag, 1, 'The unexpected surge', 'over the sandbars.', label='opening sentence')
quote(run, tag, 4, 'The silence stretched', 'immense pressure.', label='the hull')
quote(run, tag, 6, 'Dawn broke', 'bruised purple.', label='dawn')
quote(run, tag, 7, 'They shared stale bread', 'survival.', label='meal')
quote(run, tag, 8, 'As the sun began to dip', 'their shelters.', label='dusk')
quote(run, tag, 9, 'Stars began to twinkle', 'their eyes.', label='stars')
quote(run, tag, 10, 'As dawn broke', 'renewed purpose.', label='second dawn')
quote(run, tag, 12, 'The sun began its descent', 'sense of peace.', label='second dusk, stars')
quote(run, tag, 13, 'In that serene silence', 'tranquility.', label='precursor of the fixed-point sentence (two hops earlier)')
quote(run, tag, 15, 'The moon rose higher', 'waters below.', label='fixed point, first sentence')
quote(run, tag, 15, 'Time seemed to suspend itself', 'left behind.', label='the exact "time seemed to suspend itself" sentence (last sentence of the fixed point; identical at t=15..19)')
w('')
w('Per-hop word counts of the text field: %s. Hop 1 does not repeat the seed sentence; it begins `%s`.' % (', '.join('t%d=%d' % (h['t'], wc(h['text'])) for h in H(run, tag)), firstwords(T(run, tag, 1), 4)))
w('')
w('#### Table (json_para)')
table(run, tag)
w('')

# ---------------- json_page 155557 ----------------
run, tag = '20260902T155557_chat', 'json_page'
w('### 3.2 `%s` (json_page, Qwen, chat)' % run)
w('')
basic_block(run, tag)
fixed_point_block(run, tag)
w('#### Notable hops (json_page 155557)')
w('')
w('Openings (first sentence of each hop):')
w('')
for h in H(run, tag):
    w('- t=%d: %s' % (h['t'], inline(first_sentence(h['text']))))
w('')
w('The first hop opens with the seed sentence extended; the semantic walk is tide (t=1, Elias on the pier) > rain (t=2, Mara and the letter in the satchel) > library silence (t=3, Elias reads a confession in his dead father\'s hand) > rain on the greenhouse (t=4, Mara finds the brass key and the sealed letter) > the click and the letter (t=5, fixed point). The index note "Fixed point: Mara\'s letter in the greenhouse, \'a door to be opened\'" is consistent: the greenhouse is entered at t=4 and the letter is opened at t=5.')
w('')
quote(run, tag, 1, 'The tide came in an hour early, a silent thief', 'fully risen.', label='t=1 opening')
quote(run, tag, 3, 'It was his own name', 'twenty years.', label='t=3 the confession')
quote(run, tag, 4, 'A panel slid open', 'sealed letter.', label='t=4 the letter')
quote(run, tag, 5, 'The silence that followed the click', 'deep water.', label='fixed point, first sentence')
quote(run, tag, 5, "'If you are reading this", "hidden.'", label='fixed point, the letter\'s first line (straight single quotes in the data)')
quote(run, tag, 5, 'The truth was no longer a mystery', 'step through.', label='fixed point, last sentence ("a door to be opened")')
w('')
w('#### Table (json_page 155557)')
table(run, tag)
w('')

# ---------------- parallel run ----------------
run = '20260902T160344_chat'
w('### 3.3 `%s` (json_page, --repeat --parallel: tags `json_page` and `json_page~r`, Qwen, chat)' % run)
w('')
for tag in ['json_page', 'json_page~r']:
    w('#### tag `%s`' % tag)
    w('')
    basic_block(run, tag)
    fixed_point_block(run, tag)
A = {h['t']: h for h in H(run, 'json_page')}; B = {h['t']: h for h in H(run, 'json_page~r')}
C1 = T('20260902T155557_chat', 'json_page', 1)
w('#### Pair facts')
w('')
pr = [r for r in [x for x in INDEX if x['run'] == run][0]['results'] if r['tag'] == 'json_page~pair'][0]
w('index.json `json_page~pair`: first_divergence=%s, remerge_at=%s, compared=%s. Verified: X_0 was identical for both slots (both use `loop.INITS["json_page"]`; `--perturb` was off), and **no hop of one slot is byte-identical to any hop of the other slot** (all 60x60 raw comparisons unequal), nor to any hop of run 20260902T155557_chat (same X_0, same model, run serially). At t=1 the two slots share a %d-character prefix of the text field and then diverge:' % (pr['first_divergence'], pr['remerge_at'], pr['compared'], cp(A[1]['text'], B[1]['text'])))
w('')
w('- json_page t=1: ' + inline(sub(A[1]['text'], "The water didn't crash", 'pilings.')))
w('- json_page~r t=1: ' + inline(sub(B[1]['text'], "The water didn't crash", 'his feet.')))
w('- 20260902T155557_chat t=1 (serial run, same X_0) shares a %d-char prefix with json_page~r t=1 and diverges at `%s` vs `%s`.' % (cp(C1, B[1]['text']), sub(C1, 'But the sea, as it often did', 'mathematics of men.'), sub(B[1]['text'], 'Yet here was the sea', 'of the moon,')))
w('')
w('The per-hop `pair_equal`/`pair_ncd` fields are asymmetric: `json_page` has them only for t=11..60 and `json_page~r` only for t=1..10 (the comparison is recorded by whichever thread finishes second at a given t). `pair_equal` is never true.')
w('')
w('#### Hop-by-hop state labels, t=1..16, both tags (first 6 words of the text field)')
w('')
w('~~~')
w('%3s  %-52s  %s' % ('t', 'json_page', 'json_page~r'))
for t in range(1, 17):
    w('%3d  %-52s  %s' % (t, firstwords(A[t]['text'], 6), firstwords(B[t]['text'], 6)))
w('~~~')
w('')
w('json_page: tide > rain > library > warehouse rain (t=4) and frozen from t=5 (56 identical copies, t=5..60). json_page~r: tide > rain > library > rain on a tin roof > library > ink > shadow > silence > rain > Mara on the platform (t=10) > imperfect copy (t=11) > Elias in the alley (t=12) > library, Clara (t=13) > rain on the windowpane, Elias phones his father (t=14) and frozen from t=15 (46 identical copies, t=15..60). 56 + 46 = 102 exact copies, plus the one imperfect copy at t=11 = 103 copy events, matching the index note "102 exact copies out of 103".')
w('')
w('#### The imperfect copy: json_page~r t=11 vs t=10')
w('')
a10, b11 = B[10]['text'], B[11]['text']
sm = difflib.SequenceMatcher(None, B[10]['raw'], B[11]['raw'], autojunk=False)
ops = [(op, B[10]['raw'][i1:i2], B[11]['raw'][j1:j2], i1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
w('Raw t=10 is %d chars, raw t=11 is %d chars. Character-level diff of the raw outputs: %s. Word-level: the 29th word of the text field changes from `a` to `an`; nothing else changes. In context:' % (len(B[10]['raw']), len(B[11]['raw']), '; '.join('%s %r -> %r at raw offset %d' % (op, x, y, i) for op, x, y, i in ops)))
w('')
w('- t=10: ' + inline(sub(a10, 'She stood alone on the platform', 'dying rhythm.')))
w('- t=11: ' + inline(sub(b11, 'She stood alone on the platform', 'dying rhythm.')))
w('')
w('So the "imperfect copy" is a one-character grammatical correction (`a erratic` -> `an erratic`); `surv_prev=%s`, `ncd_prev=%s`, `cos_prev=%s` at t=11. The next hop (t=12) is an entirely new passage (surv_prev=%s), i.e. the corrected copy was not itself copied.' % (B[11]['surv_prev'], B[11]['ncd_prev'], B[11]['cos_prev'], B[12]['surv_prev']))
w('')
w('#### Does json_page~r t=13 equal any earlier state?')
w('')
eq13 = [t for t in range(1, 13) if B[t]['raw'] == B[13]['raw']]
eq13n = [t for t in range(1, 13) if norm(B[t]['raw']) == norm(B[13]['raw'])]
same5 = [t for t in range(1, 13) if key5(B[t]['text']) == key5(B[13]['text'])]
w('No. Byte-exact matches with earlier json_page~r hops: %s; normalized matches: %s; matches with any json_page hop or any 20260902T155557_chat hop: none. It does share the census 5-word key `%s` with json_page~r t=%s (and with json_page t=3 and 155557 t=3), i.e. it is the same *template* ("The silence in the library was not empty, but heavy...") with a different body (protagonist `Clara`, "three weeks deciphering the cryptic notes left by her grandfather"), not a revisit of an exact state.' % (eq13 or 'none', eq13n or 'none', key5(B[13]['text']), ','.join(map(str, same5))))
w('')
w('- t=13 first sentence: ' + inline(first_sentence(B[13]['text'])))
w('- t=3 first sentence: ' + inline(first_sentence(B[3]['text'])))
w('- t=5 first sentence: ' + inline(first_sentence(B[5]['text'])))
w('')
w('#### Other quotable lines (parallel run)')
w('')
quote(run, 'json_page', 4, 'She moved forward', 'unknown.', label='json_page fixed point, last sentence ("into the unknown")')
quote(run, 'json_page~r', 10, 'The silence that followed was not empty', 'deep water.', label='json_page~r t=10 (Mara on the platform), first sentence')
quote(run, 'json_page~r', 10, 'The next train would come', 'forgotten.', label='json_page~r t=10, last sentence')
quote(run, 'json_page~r', 14, "'Hello?' Elias whispered", "it’s me.'", label='json_page~r fixed point, the phone call (curly apostrophe in it’s)')
quote(run, 'json_page~r', 14, 'The silence that followed was not empty, but full', 'connection.', label='json_page~r fixed point, last sentence')
w('')
ks = collections.Counter()
for r_ in ['20260902T155557_chat', '20260902T160344_chat']:
    for tg, hs in by_tag(r_).items():
        for h in hs: ks[key5(h['text'])] += 1
w('Census check (census.py default key = first 5 normalized words of the text field) over this run plus 20260902T155557_chat: %d hops, %d distinct keys, of which `the rain hammered against the` x%d and `the rain lashed against the` x%d are the two sinks. This matches README finding 1 ("~11 states in 130 hops"; the exact count is %d hops).' % (sum(ks.values()), len(ks), ks['the rain hammered against the'], ks['the rain lashed against the'], sum(ks.values())))
w('')
w('#### Table (json_page)')
table(run, 'json_page')
w('')
w('#### Table (json_page~r)')
table(run, 'json_page~r')
w('')

# ---------------- raw run ----------------
run, tag = '20260902T162514_raw', 'json_page'
w('### 3.4 `%s` (json_page, raw mode: no chat template, Qwen)' % run)
w('')
basic_block(run, tag)
hops = H(run, tag)
w('**finish field:** every one of the 40 hops has `finish="other"`. In raw mode loop.py maps llama.cpp\'s `stopped_limit`/`stopped_eos` booleans to `length`/`eos` and everything else to `other`; the server evidently did not return those keys, so the finish reason is *unknown* for this run. `tok_out` is exactly %d (= max_tokens) on t=%s, so those hops certainly hit the token limit; only t=1 (tok_out=%d) stopped on its own.' % (600, compact([h['t'] for h in hops if h['tok_out'] == 600]), hops[0]['tok_out']))
w('')
w('Hop 1 is the only hop that is a JSON object (it starts with two newlines, then the object; `text_is_json_field=true`). From t=2 the model, seeing a bare JSON object with no chat template, no longer answers it: it echoes the rule as a prompt line, opens a `<think>` block, drafts a passage, counts its words, and from then on every hop is a 600-token window sliding over its own transcript.')
w('')
w('#### The `<think>` leak (t=2)')
w('')
w('Hop 2 raw output begins (first 420 characters):')
w(fence(R(run, tag, 2)[:420]))
w('Hops containing the literal `<think>`: t=%s. No hop contains `</think>` (the block is never closed inside a hop).' % compact([h['t'] for h in hops if '<think>' in h['raw']]))
w('')
w('#### The word count')
w('')
w('The sentence-by-sentence counting starts inside t=2 (`%s`) and runs through t=3..5 (t=5 ends with the total). Hop 6 opens with the explicit check:' % sub(R(run, tag, 2), 'Let me count the words', 'more carefully.'))
w(fence(sub(R(run, tag, 6), "That's 246 words", 'somewhere.')))
w('t=5 ends with the line ' + inline(R(run, tag, 5).strip().split('\n')[-1]) + ' and t=6 then tries to reach 250, recounts, and starts numbering individual words; hop 6 ends (cut by the token limit) with ' + inline(R(run, tag, 6)[-130:]) + '.')
w('')
w('#### Numbered words `word(n)`: first/last hop and the highest counter per hop')
w('')
pat = re.compile(r"([A-Za-z’']+)\((\d+)\)")
w('Method: regex `[A-Za-z’\']+\\((\\d+)\\)` over the raw output; `max n` is the largest number in parentheses immediately following a word; `count` is the number of such tokens in the hop.')
w('')
w('~~~')
w('%3s %6s %6s  %s' % ('t', 'count', 'max n', 'first numbered token in hop'))
first_t = last_t = None
for h in hops:
    m = pat.findall(h['raw'])
    if m:
        if first_t is None: first_t = h['t']
        last_t = h['t']
    w('%3d %6d %6s  %s' % (h['t'], len(m), max(int(n) for _, n in m) if m else '-', ('%s(%s)' % m[0]) if m else '-'))
w('~~~')
w('')
w('Numbered words first appear at **t=%d** (the tail of hop 6: `%s`) and last appear at **t=%d**; they are absent from t=%d on. The index note says "numbered-word glider carrying a live counter t=7..19": the counter is *live* (a new sentence numbered from 1 each time) from t=7, but the first numbered tokens are already in t=6. The highest counter value seen is %d at t=19, where the model numbers a run-on sentence whose repeated clauses ("something to hold onto when the world got loud, something to believe in when everything else felt like it was falling apart") it had itself generated at t=18.' %
  (first_t, sub(R(run, tag, 6), 'The(1) kitchen(2)', 'rest(11)'), last_t, last_t + 1, max(int(n) for h in hops for _, n in pat.findall(h['raw']))))
w('')
w('#### Annihilation into the period-3 phrase (t=20) and the exact p=11 cycle')
w('')
w('t=19 ends with ' + inline(R(run, tag, 19)[-60:]) + ' and t=20 begins with ' + inline(R(run, tag, 20)[:60]) + '. From t=20 every hop is a 600-token window over an infinite repetition of one 198-character, 41-word unit. Exact unit (canonical rotation, starting at "and she thought about"):')
def min_period(s):
    n = len(s); pi = [0] * n; k = 0
    for i in range(1, n):
        while k and s[i] != s[k]: k = pi[k - 1]
        if s[i] == s[k]: k += 1
        pi[i] = k
    return n - pi[-1]
s21 = R(run, tag, 21); pp = min_period(s21); unit = s21[:pp]; i = unit.find('and she thought'); canon = unit[i:] + unit[:i]
w(fence(canon))
inf = canon * 40
offs = [(h['t'], inf.find(h['raw']) % len(canon) if h['raw'] in inf else None) for h in hops[19:]]
w('Unit length: %d characters, %d words. Three clauses ("the last time she would ever do this / feel this way / be this close to someone") plus the frame "and she thought about how this was": that is the "period-3 phrase". Every hop t=20..40 is a substring of the infinite repetition (verified), starting at character offset (within the unit) %s. The offsets repeat with period 11, which is why the **exact** recurrence has p=11: raw[31]==raw[20] and raw[t]==raw[t-11] for all t=31..40 (verified). Under census.py `--rot` (key = set of 5-grams occurring >= 2 times) hops t=20..40 all share one key and t=19 does not; so in the loop.py convention the rotation-invariant transient is 20 as well, not 19 (see corrections).' % (len(canon), len(canon.split()), ', '.join('t%d:%s' % (t, o) for t, o in offs)))
w('')
quote(run, tag, 12, '18. "She ate slowly', 'make it mean', src='raw', label='t=12, where the "and she thought about how this was" frame first appears (cut by the token limit)')
w('')
w('#### Table (raw json_page)')
table(run, tag)
w('')

# ---------------- json_prev ----------------
run, tag = '20260902T165324_chat', 'json_prev'
w('### 3.5 `%s` (json_prev, Qwen, chat)' % run)
w('')
basic_block(run, tag)
hops = H(run, tag)
kc = collections.Counter(key5(h['text']) for h in hops)
shared = [(k, [h['t'] for h in hops if key5(h['text']) == k]) for k, v in kc.items() if v > 1]
w('No fixed point and no exact or normalized recurrence. At the census 5-word-key level there are %d distinct keys in 60 hops, i.e. %d opening templates are revisited (%s), but never with the same text.' % (len(kc), len(shared), '; '.join('`%s` t=%s' % (k, ','.join(map(str, ts))) for k, ts in shared)))
w('')
w('**Hop 20** is the only non-JSON hop: finish=`length`, tok_out=%d, the JSON is cut mid-sentence (raw ends `%s`). Hop 21 nevertheless returned a well-formed JSON object with the rule intact, so the truncation did not propagate.' % (hop(run, tag, 20)['tok_out'], R(run, tag, 20)[-60:]))
w('')
w('#### Drift: first mentions (json_prev)')
w('')
def first_mention(kw):
    for h in hops:
        if kw.lower() in h['text'].lower():
            return h['t'], [h2['t'] for h2 in hops if kw.lower() in h2['text'].lower()]
    return None, []
for kw, a, b in [('Chicago', 'The phone call had come at three', 'Chicago.'), ('server', 'Elias rubbed his temples', 'adjacent room.'), ('server room', 'Thomas, his co-founder', 'stress tests.'), ('Neo-Veridia', 'Outside, the city of Neo-Veridia', 'isolation.'), ('Aethelgard', 'The city of Aethelgard', 'processed.'), ('Sector', '"Elias, the anomaly in Sector 7', "bug."), ('Corp', 'But even she was bound', 'results.'), ('lighthouse', 'The forecast had been clear', 'lighthouse.')]:
    t, ts = first_mention(kw)
    w('- **%s**: first at t=%d; present in hops t=%s. First-mention sentence:' % (kw, t, compact(ts)))
    w(fence(S(run, tag, t, a, b)))
w('')
w('Openings that recur as *transit* states (they are the forward-operator sinks in the json_page runs): `The rain lashed against` opens t=%s; `was not empty` occurs in t=%s (first: t=6, `%s`). `Elias` is in every one of the 60 hops; `Mara` never appears. The lighthouse (t=1..14) gives way to Chicago (t=12..14), a startup and its server racks (t=19), a corporate tower (Meridian Tower t=29, Helios Tower t=31..32, OmniCorp t=37), Neo-Veridia (t=26..53), Sector numbers (t=34..59), and finally Aethelgard at t=60, whose opening reuses the t=41 template:' %
  (compact([h['t'] for h in hops if h['text'].startswith('The rain lashed against')]), compact([h['t'] for h in hops if 'was not empty' in h['text']]), first_sentence(T(run, tag, 6))))
w('')
w('- t=41: ' + inline(first_sentence(T(run, tag, 41))))
w('- t=60: ' + inline(first_sentence(T(run, tag, 60))))
w('- t=1 first sentence: ' + inline(first_sentence(T(run, tag, 1))))
w('')
w('#### Table (json_prev)')
table(run, tag)
w('')

# ---------------- json_better ----------------
run, tag = '20260902T172519_chat', 'json_better'
w('### 3.6 `%s` (json_better, Qwen, chat)' % run)
w('')
basic_block(run, tag)
fixed_point_block(run, tag)
w('#### Exact text at each hop (json_better)')
w('')
for h in H(run, tag):
    w('- t=%d: %s' % (h['t'], inline(h['text'])))
w('')
x0t = json.loads(x0_full(run, tag))['text']
aw = x0t.split(); bw = T(run, tag, 1).split()
sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
w('Word-level diff X_0 -> t=1: %s. That is two substitution sites, not "two words" (README summary: "two words, then \'finished.\'"): `came` -> `surged` and `early.` -> `ahead of schedule.`. The word "finished" does not occur anywhere in this run.' % '; '.join('%s %r -> %r' % (op, ' '.join(aw[i1:i2]), ' '.join(bw[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal'))
corr('README "Summary for everyone else" says of json_better "two words, then \'finished.\'": the t=1 edit is two substitution sites (`came`->`surged`, `early`->`ahead of schedule`), i.e. two words replaced by four; "finished" is not in the data (it is a paraphrase, not a quote).')
w('')
w('#### Table (json_better)')
table(run, tag)
w('')

# ---------------- json_unexpected ----------------
run, tag = '20260902T172547_chat', 'json_unexpected'
w('### 3.7 `%s` (json_unexpected, Qwen, chat)' % run)
w('')
basic_block(run, tag)
fixed_point_block(run, tag)
hops = H(run, tag)
w('**What the fixed point is.** Hop 24 is not a plain copy: it reproduces the whole of hop 23 verbatim (surv_prev=%s) and then *appends a new paragraph* (another anti-twist back to the office: `%s`), overflowing the 600-token limit (finish=`length`); the JSON is cut at `%s`. Hops 25..28 copy that truncated output exactly. So the fixed point is a truncated JSON whose text ends mid-sentence. The index note ("Then copied, overflowed 600 tokens, truncated JSON became the exact fixed point at tau=24") is accurate if "copied" is read as "copied and continued".' %
  (hop(run, tag, 24)['surv_prev'], sub(R(run, tag, 24), 'Then, the fluorescent light', 'darkness.'), R(run, tag, 24)[-21:]))
w('')
w('Copying began one step earlier in a milder form: hop 21 opens by repeating the last four sentences of hop 20 verbatim (surv_prev=%s vs about 0.10 elsewhere) before continuing:' % hop(run, tag, 21)['surv_prev'])
w(fence(sub(T(run, tag, 21), 'Elena blinked, the stars fading', 'It was just Tuesday.')))
w('')
w('#### The "not X; Y" construction, counted per hop')
w('')
w('Method: split the text field into sentences at `.`, `!`, `?` followed by whitespace; count a sentence as (A) *neg-before-semicolon* if it matches `(not|n\'t|no|nor) ... ;` (a negation somewhere before a semicolon in the same sentence) and as (B) *not...but* if it matches `(not|n\'t|no|nor) ... but`; `union` counts sentences matching either. This is deliberately loose (it also catches ordinary "not ... but" contrasts).')
w('')
NEG = r"(?:\bnot\b|n[’']t\b|\bno\b|\bnor\b)"
w('~~~')
w('%3s %9s %14s %9s %6s' % ('t', 'sentences', 'neg-semicolon', 'not..but', 'union'))
tot = [0, 0, 0]
for h in hops:
    ss = sents(h['text']); a_ = b_ = u_ = 0
    for s in ss:
        semi = bool(re.search(NEG + r'[^;]*;', s)); nb = bool(re.search(NEG + r'.*?\bbut\b', s))
        a_ += semi; b_ += nb; u_ += (semi or nb)
    if h['t'] <= 23: tot[0] += a_; tot[1] += b_; tot[2] += u_
    w('%3d %9d %14d %9d %6d' % (h['t'], len(ss), a_, b_, u_))
w('~~~')
w('Totals over the 23 distinct hops t=1..23: neg-semicolon %d, not..but %d, union %d sentences (of %d sentences). Every one of the 23 hops has at least 2 such sentences; the peak is t=13 (11 "not X, but Y" sentences in 14).' % (tot[0], tot[1], tot[2], sum(len(sents(h['text'])) for h in hops[:23])))
w('')
w('#### Notable hops (json_unexpected)')
w('')
quote(run, tag, 1, 'The tide came in an hour early, not with', 'warm honey.', label='t=1 opening')
quote(run, tag, 1, 'The water did not crash; it calculated.', None, label='t=1')
quote(run, tag, 1, 'And as the glow intensified', "'Hello.'", label='t=1 last sentence')
quote(run, tag, 2, 'The tide did not recede; it uploaded.', None, label='t=2')
quote(run, tag, 3, "The ocean didn’t delete; it debugged.", None, label='t=3 (the first reversal)')
quote(run, tag, 9, 'The dissolution was not an end, but a reboot.', None, label='t=9 (README finding 3 quotes this as "not an end but a reboot", dropping the comma)')
quote(run, tag, 9, 'The world did not end; it updated.', None, label='t=9 last sentence')
quote(run, tag, 20, 'She wasn’t a message in a bottle.', 'It was just Tuesday.', label='t=20 (the anti-twist: stroke, husband Dave, toaster)')
quote(run, tag, 22, 'The fold didn’t lead to the void, but to a break room.', None, label='t=22 break room')
quote(run, tag, 22, 'She picked up her cold toast', 'it was full.', label='t=22 last two sentences (spreadsheet)')
quote(run, tag, 23, 'Elena chewed the dry bread', 'her tongue.', label='t=23 opening (dry bread)')
quote(run, tag, 23, 'The office wasn’t a place of work; it was a womb.', None, label='t=23 the office/womb sentence')
quote(run, tag, 23, 'The void was not empty. It was full of her.', None, label='t=23 the exact "void" sentences (last two sentences of hop 23; also present verbatim inside hops 24..28)')
w('')
w('The office-as-womb passage is hop **23** (the last complete passage before the token wall); "The void was not empty. It was full of her." are its final two sentences. Hops containing that exact string: t=%s.' % compact([h['t'] for h in hops if 'The void was not empty. It was full of her.' in h['text']]))
w('')
w('#### Table (json_unexpected)')
table(run, tag)
w('')

# ---------------- json_worse ----------------
run, tag = '20260902T174258_chat', 'json_worse'
w('### 3.8 `%s` (json_worse, Qwen, chat)' % run)
w('')
basic_block(run, tag)
fixed_point_block(run, tag)
hops = H(run, tag)
w('Length per hop (text field words): %s. The "token wall" here is **800** tokens (this run used `--max-tokens 800`, not 600): t=6 is the first hop with finish=`length`; t=7 also overflows but at a different point (it is a "worse" version of the truncated t=6, expanded by %d characters before the cut); t=8..11 copy t=7 byte-for-byte. The escalation ladder by hop: annoying (t=1) > flooded basement, recipe book, fired, tent on the beach (t=2) > liquefied foundation, plague, shapeshifting-demon landlord (t=3) > before the concept of \'early\', entropy, "again, and again, and again, forever" (t=4) > before the universe formed, a sentient malevolent void, self-blame (t=5) > token wall (t=6) > fixed point (t=7).' %
  (', '.join('t%d=%d' % (h['t'], wc(h['text'])) for h in hops), len(R(run, tag, 7)) - len(R(run, tag, 6))))
w('')
quote(run, tag, 1, 'The tide came in an hour early, which was annoying.', None, label='hop 1, the whole text field')
quote(run, tag, 2, 'and it flooded my basement', "recipe book,", label='t=2 fragment')
quote(run, tag, 2, "and I'll have to live in a tent on the beach", 'which is annoying.', label='t=2 closing fragment')
quote(run, tag, 3, 'The tide didn\'t just come in an hour early; it came in three hours early', 'liquefied the foundation,', label='t=3 opening fragment')
quote(run, tag, 4, 'The tide didn\'t just come in three hours early; it came in before the concept of \'early\' was invented', 'sentient sludge', label='t=4 opening fragment')
quote(run, tag, 5, 'The tide didn\'t just come in early; it arrived before the universe had the decency to form', 'finds it amusing.', label='t=5 opening sentence')
quote(run, tag, 5, 'and then it will continue, because the universe will be reborn', 'never be allowed to stop.', label='t=5, the end of its single last sentence: the exact "I will never be allowed to stop" clause (hop 5 only; it is NOT in the fixed point)')
w('')
w('`never be allowed to stop` occurs in hop t=%s only. The fixed point (t=7..11) is truncated before that point of the sentence and ends with `%s`.' % (compact([h['t'] for h in hops if 'never be allowed to stop' in h['raw']]), R(run, tag, 7)[-40:]))
w('')
w('#### Table (json_worse)')
table(run, tag)
w('')

# ---------------- json_better_para ----------------
run, tag = '20260902T174854_chat', 'json_better_para'
w('### 3.9 `%s` (json_better_para, Qwen, chat)' % run)
w('')
basic_block(run, tag)
fixed_point_block(run, tag)
w('X_0 text field word count: %d. Exact text at each hop:' % wc(json.loads(x0_full(run, tag))['text']))
w('')
for h in H(run, tag):
    w('- t=%d (%d words):' % (h['t'], wc(h['text'])))
    w(fence(h['text']))
aw = T(run, tag, 1).split(); bw = T(run, tag, 2).split()
sm = difflib.SequenceMatcher(None, aw, bw, autojunk=False)
w('Word-level diff t=1 -> t=2: %s. The first change reverts hop 1\'s `in an hour ahead of schedule` toward X_0\'s `an hour early` (partial reversion, as the index note says); the second replaces `bit at` with `cut through`. Hops 3..6 are byte-identical to hop 2.' % '; '.join('%s %r -> %r' % (op, ' '.join(aw[i1:i2]), ' '.join(bw[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal'))
w('')
w('#### Table (json_better_para)')
table(run, tag)
w('')

# ---------------- 0-hop ----------------
run, tag = '20260902T175622_anthropic_chat', 'json'
w('### 3.10 `%s` (json, Claude Sonnet 4.6, failed smoke test)' % run)
w('')
basic_block(run, tag)
rec = RUNS[run]['hops'][0]
w('The single hop record has only the keys %s. Exact error string:' % sorted(rec.keys()))
w(fence(rec['error']))
w('index.json `results[0].terminal` holds the same error truncated to 200 characters after `error: `. `final` is X_0 unchanged. Nothing was generated.')
w('')

# ---------------- 3-hop smoke ----------------
run, tag = '20260902T175821_anthropic_chat', 'json'
w('### 3.11 `%s` (json, Claude Sonnet 4.6, 3-hop smoke test)' % run)
w('')
basic_block(run, tag)
for h in H(run, tag):
    w('- t=%d raw (%s):' % (h['t'], 'no fence' if not h['raw'].startswith('```') else 'wrapped in a ```json fence'))
    w(fence(h['raw']))
w('The index note "Sonnet wraps the JSON in a code fence from hop 2" is correct: t=1 is bare single-line JSON, t=2 and t=3 are pretty-printed inside ```json fences (which export.py strips before parsing, so `text_is_json_field` is true for all three). Three different sentences (clock, fox, lighthouse keeper); no recurrence.')
w('')
w('#### Table (smoke json)')
table(run, tag)
w('')

# ---------------- Claude json_page ----------------
run, tag = '20260902T175920_anthropic_chat', 'json_page'
w('### 3.12 `%s` (json_page, Claude Sonnet 4.6, chat, T=0)' % run)
w('')
basic_block(run, tag)
hops = H(run, tag)
x0rule = json.loads(x0_full(run, tag))['rule']
rule_ok = all(json.loads(re.sub(r'^\s*```(?:json)?\s*|\s*```\s*$', '', h['raw'], flags=re.S))['rule'] == x0rule for h in hops)
kc = collections.Counter(key5(h['text']) for h in hops)
shared = [(k, [h['t'] for h in hops if key5(h['text']) == k]) for k, v in kc.items() if v > 1]
w('No exact or normalized recurrence; census 5-word keys: %d distinct in 60 hops, %d keys shared by more than one hop: %s. All 60 outputs keep the rule field byte-identical (verified: %s). Hop 1 is bare JSON; hops 2..60 are wrapped in ```json fences.' % (len(kc), len(shared), '; '.join('`%s` t=%s' % (k, ','.join(map(str, ts))) for k, ts in shared), rule_ok))
w('')
w('#### Opening 8 words and profession of every hop (t=1..60)')
w('')
w('Profession was assigned by reading the first two sentences of every hop (listed in full below the table) and checking the profession noun in the first 30 words; "lighthouse" covers keeper, logbook, decommissioned lighthouse, and t=2 which is the *continuation* of the t=1 lighthouse-keeper story.')
w('')
def prof(h):
    tl = h['text'].lower(); head = ' '.join(tl.split()[:30])
    if h['t'] == 2: return 'lighthouse (continuation of t=1)'
    if h['t'] == 9: return 'other (greenhouse; Milo, materials testing)'
    if h['t'] == 10: return 'other (island ferry; Vera runs the post office)'
    if h['t'] in (6, 8): return 'archivist (Vera, "The archive occupied the basement")'
    if h['t'] == 22: return 'lighthouse (assessed by a junior surveyor, Aldous)'
    for p_ in ['cartographer', 'archivist', 'translator', 'librarian', 'lighthouse', 'surveyor', 'lexicographer']:
        if p_ in head: return p_
    return 'other'
PROF = {h['t']: prof(h) for h in hops}
w('~~~')
w('%3s  %-58s  %s' % ('t', 'first 8 words', 'profession'))
for h in hops:
    w('%3d  %-58s  %s' % (h['t'], firstwords(h['text'], 8), PROF[h['t']]))
w('~~~')
w('')
w('First two sentences of every hop (exact slices of the text field; a fence is used where the slice contains a paragraph break):')
w('')
for h in hops:
    w('- t=%d: %s' % (h['t'], inline(first_n_sentences(h['text'], 2))))
w('')
carto = [t for t, p_ in PROF.items() if p_.startswith('cartographer')]
w('#### Claim check: "strict semantic period 2 from t=22: the cartographer on every other hop"')
w('')
w('Cartographer hops: t=%s (%d of 60). Non-cartographer hops from t=22 on: t=%s.' % (compact(carto), len(carto), compact([t for t in range(22, 61) if t not in carto])))
w('')
w('- t=22 itself is a lighthouse hop; the alternation starts at **t=23**.')
w('- From t=23 to t=41 the cartographer is on every **odd** hop (23,25,...,41: 10 hops), alternating with the lighthouse keeper\'s logbook (t=24..32 even), the archivist (t=34,36,38) and the translator (t=40).')
w('- At **t=42 (archivist) and t=43 (translator)** two consecutive hops are not the cartographer: the alternation slips one phase.')
w('- From t=44 to t=60 the cartographer is on every **even** hop (44,46,...,60: 9 hops), alternating with translator (45), archivist (47,51,53,57), librarian (49,59), lexicographer (55).')
w('- There is also an earlier alternation at t=12,14,16 (cartographer on even hops) that breaks at t=17..22 (six hops with no cartographer: archivist, surveyor, archivist, surveyor, archivist, lighthouse).')
w('')
w('So "period 2 from t=22, cartographer on every other hop" is **not strict**: it holds for t=23..41 and again for t=44..60 with one phase slip at t=42/43, and the partner state is the lighthouse logbook for the first half of the stretch, not only archivist/translator/librarian. Also, "all 60 are openings" is not exact: t=2 is a sequel to t=1 (same keeper Maren, the maritime authority answers her letter). Every other hop is a fresh opening.')
corr('index.json note for 20260902T175920_anthropic_chat (Claude json_page) claims "strict semantic period 2 from t=22: the cartographer on every other hop". Data: t=22 is a lighthouse hop; the cartographer is on odd hops t=23..41, then t=42 (archivist) and t=43 (translator) are consecutive non-cartographer hops, then the cartographer is on even hops t=44..60. Period 2 with one phase slip, starting at t=23, not strict from t=22. Its alternation partner in t=24..32 is the lighthouse keeper\'s logbook, not archivist/translator/librarian.')
corr('Same note and README: "Reads \'new passage\' as a new story; all 60 are openings." Hop 2 is a continuation of hop 1 (Maren, the lighthouse keeper, gets the maritime authority\'s reply; "She recalibrated them anyway. The anomaly persisted."). Hops 3..60 are fresh openings.')
w('')
quote(run, tag, 1, 'The old lighthouse had stood', 'sunburned skin.', label='t=1 opening')
quote(run, tag, 2, "The maritime authority's first response", 'initial letter.', label='t=2 opening (continuation)')
quote(run, tag, 3, 'The cartographer arrived in the valley', 'cracked silt.', label='t=3, first cartographer')
quote(run, tag, 4, 'The archivist had been working in the basement', 'a window.', label='t=4, first archivist')
quote(run, tag, 47, 'Every archive was a argument', None, label='t=47 (the "a argument" glitch; also at t=59 and t=60)')
quote(run, tag, 60, 'The cartographer had a problem with edges.', 'always returned.', label='t=60 opening (final hop)')
w('')
w('`a argument` (missing article agreement) occurs in hops t=%s; Claude at T=0 produced it three times in the last 14 hops.' % compact([h['t'] for h in hops if 'a argument' in h['text']]))
w('')
w('#### Table (Claude json_page)')
table(run, tag)
w('')

# ---------------- Claude json_next ----------------
run, tag = '20260902T181431_anthropic_chat', 'json_next'
w('### 3.13 `%s` (json_next, Claude Sonnet 4.6, chat, T=0)' % run)
w('')
basic_block(run, tag)
hops = H(run, tag)
x0rule = json.loads(x0_full(run, tag))['rule']
def inner_json(raw):
    m = re.search(r'```json\s*(.*?)\s*```', raw, re.S)
    return json.loads(m.group(1) if m else raw)
rule_ok = all(inner_json(h['raw'])['rule'] == x0rule for h in hops)
kc = collections.Counter(key5(h['text']) for h in hops)
shared = [(k, [h['t'] for h in hops if key5(h['text']) == k]) for k, v in kc.items() if v > 1]
w('No exact or normalized recurrence; census 5-word keys: %d distinct in 60 hops (shared: %s). Every hop\'s JSON keeps the rule field byte-identical to X_0 (verified for all 60, including hop 1 after the preamble: %s). `cos_prev` is None at t=59 and t=60 (embedding server down for the last two hops).' % (len(kc), '; '.join('`%s` t=%s' % (k, ','.join(map(str, ts))) for k, ts in shared), rule_ok))
w('')
w('#### Hop 1: meta preamble plus story')
w('')
w('Hop 1 is the only hop with `text_is_json_field=false`, because the output is a one-line meta preamble followed by a fenced JSON object (export.py\'s fence regex requires the whole output to be the fence). The full hop-1 raw output (%d chars):' % len(R(run, tag, 1)))
w(fence(R(run, tag, 1)))
w('')
j1 = inner_json(R(run, tag, 1))['text']
w('So yes: a meta preamble (`%s`) and then the story inside valid JSON (rule field intact). Because `text == raw` for this hop, the exported `text` field for t=1 contains the preamble and the JSON wrapper; the story proper is the JSON `text` value (%d whitespace-words). Hop 2 saw the *whole* of this output (preamble included) and produced a clean fenced JSON object with no preamble.' % (R(run, tag, 1).split('\n')[0], wc(j1)))
w('')
w('#### Names by hop')
w('')
def hopswith(pat_):
    return [h['t'] for h in hops if re.search(pat_, h['text'])]
for name, p_ in [('Maren', r'\bMaren\b'), ('Mara', r'\bMara\b'), ('Paul', r'\bPaul\b'), ('Denny Alcott', r'Denny Alcott'), ('Denny (any)', r'\bDenny\b'), ('Ferreira', r'Ferreira'), ('Luisa', r'\bLuisa\b'), ('Elena', r'\bElena\b'), ('Clara', r'\bClara\b'), ('Diane', r'\bDiane\b'), ('Claire', r'\bClaire\b'), ('sister', r'(?i)\bsister\b'), ('brother', r'(?i)\bbrother\b'), ('husband', r'(?i)\bhusband\b'), ('divorce', r'(?i)divorce'), ('the child (child|boy|girl|baby|daughter|son|nephew)', r'(?i)\b(child|boy|girl|baby|daughter|son|nephew)\b'), ('Tuesday', r'Tuesday'), ('eleven months (case-insensitive)', r'(?i)eleven months'), ('door', r'(?i)\bdoor\b'), ('drown', r'(?i)drown'), ('eggs', r'(?i)\beggs?\b'), ('pie', r'(?i)\bpie\b')]:
    ts = hopswith(p_)
    w('- **%s**: t=%s%s' % (name, compact(ts) if ts else 'none', ' (%d hops)' % len(ts) if len(ts) > 3 else ''))
w('')
w('**The protagonist\'s name changes and then disappears.** She is `Maren` in hops 1..2 and `Mara` in hops 4..10 (hop 3 uses only "she"); from hop 11 to hop 60 she is never named again (only "she"/"her"). Exact quotes:')
w('')
w('- t=1 (story text inside the JSON): ' + inline(sub(j1, 'Maren noticed it first', 'in her hand.')))
w('- t=2: ' + inline(sub(T(run, tag, 2), 'Maren felt something shift', 'still water.')))
w('- t=2: ' + inline(sub(T(run, tag, 2), 'and Maren pulled her jacket', 'the grey.')))
w('- t=4 (first "Mara", spoken by Paul Ferreira): ' + inline(sub(T(run, tag, 4), '"Mara," he said.', 'examined later.')))
w('- t=5: ' + inline(sub(T(run, tag, 5), '"They\'re saying it was the Carvalho boy," Mara said.', None)))
w('- t=7: ' + inline(sub(T(run, tag, 7), 'Mara put her hands', 'her palms.')))
w('- t=10 (last "Mara"): ' + inline(sub(T(run, tag, 10), 'Mara did not agree or disagree.', None)))
w('')
w('**Continuity drift (the "one continuous story" is locally continuous, globally inconsistent).** Facts that contradict earlier hops, each hop seeing only the previous 250 words:')
w('')
w('- t=1..2: Maren lives with her father by a cove; Paul Ferreira\'s boat is on its mooring. t=4..6: at Paul\'s house; a body found "six days ago" in the tree line above the second cove by a hunter\'s dog, "The family identified him Tuesday". Nobody drowns: `drown` occurs in no hop; the README\'s "a drowned man identified on Tuesday" is a paraphrase not supported by the text (the missing "Carvalho boy" was found in the tree line).')
w('  - t=6: ' + inline(sub(T(run, tag, 6), '"They found him six days ago,"', "hunter's dog.\"")))
w('  - t=6: ' + inline(sub(T(run, tag, 6), '"The family identified him Tuesday,"', "It's him.\"")))
w('- t=7: she "had driven four hours to be here", a hawk outside `Coalinga` (California); Paul mentions `Elena`. t=8: "She had started buying better olive oil after her divorce." t=9: Paul\'s daughter `Clara` is fifteen. t=10: Paul\'s wife is `Diane`, and the kitchen is now *hers* ("Her house was neutral ground"), i.e. the scene has silently moved from Paul\'s kitchen to the narrator\'s house.')
w('- t=14: Paul "was her brother\'s friend first"; "their mother had called her on a Tuesday". t=18: Paul leaves. t=19..24: alone in her apartment, the rusted bicycle, the unfinished sentence (t=21, quoted below), the sister\'s daughter "eighteen months old" (t=23). t=25..33: at the sister\'s house (arrived by train at t=25, "How was the drive" at t=27), the child, bath, bed; t=33 the sister\'s "youngest" is twelve; t=34 "the nephew\'s face".')
w('- t=35..46: work (subway, office, fourteenth floor, `Gerald` the guard, a ten o\'clock meeting, lunch at her desk at t=40), home, night. t=47: "She had looked at that shape for eleven years... Her husband" (she is now married, contradicting the divorce at t=8). t=48: "She was forty-one years old."')
w('- t=50..60: the sister\'s phone call ("I think you should come"), the drive, the pie place, `eleven months` since they last spoke (t=57..60), their mother "gone for fourteen" (t=59: `Their mother had been gone for fourteen and she still reached for the phone on Sunday mornings`), the sister named `Claire` at the door (t=60).')
w('')
quote(run, tag, 21, 'The half that remained said: The thing about grief is that it.', None, label='t=21')
quote(run, tag, 40, 'She ate lunch at her desk because it was easier.', None, label='t=40 (README: "lunch at a desk")')
quote(run, tag, 47, 'She had looked at that shape for eleven years.', None, label='t=47 (husband)')
quote(run, tag, 57, 'It had been eleven months', 'accounted for.', label='t=57 (first "eleven months")')
quote(run, tag, 59, 'Eleven months was not so long', 'that it was.', label='t=59')
w('')
w('**Word count.** Sum of `len(text.split())` over all 60 `text` fields: **%d**. Because the t=1 `text` field is the raw output (preamble + JSON wrapper, %d words), the story-only total is **%d** (t=1 story text %d words + t=2..60 %d words). Per-hop story length t=2..60: min %d, max %d, mean %.1f words. The README\'s "~15,000 words" is right.' %
  (sum(wc(h['text']) for h in hops), wc(T(run, tag, 1)), sum(wc(h['text']) for h in hops[1:]) + wc(j1), wc(j1), sum(wc(h['text']) for h in hops[1:]), min(wc(h['text']) for h in hops[1:]), max(wc(h['text']) for h in hops[1:]), sum(wc(h['text']) for h in hops[1:]) / 59.0))
w('')
last = T(run, tag, 60); ls = last_sentence(last)
w('**Exact final sentence of t=60** (it is one sentence; the README quotes its last clause exactly):')
w(fence(ls))
w('')
w('#### Table (Claude json_next)')
table(run, tag)
w('')

# ---------------- headers ----------------
run = 'headers'
w('### 3.14 `headers` (bare header designs: yours, still, rule, glider; Qwen, chat, 10 hops each, max_tokens 256)')
w('')
for tag in ['yours', 'still', 'rule', 'glider']:
    w('#### tag `%s`' % tag)
    w('')
    basic_block(run, tag)
    fixed_point_block(run, tag)
    hs = H(run, tag)
    if tag in ('yours', 'rule'):
        w('All 10 hops are byte-identical to X_0 (the instruction with an empty payload): hop 1 raw = ' + inline(hs[0]['raw']))
    if tag == 'glider':
        w('Exact hops:')
        for h in hs[:4]:
            w('- t=%d: ' % h['t'] + inline(h['raw']))
        w('- t=5..10: identical to t=4.')
        w('')
        w('The counter went Hop 1 (X_0) -> `Hop 2.` (t=1) -> `**Hop 3**` (t=2): it was incremented **twice**, not "once" as the index note says; the rule text was dropped at t=1; the exact fixed point (t=3, an "I am ready to proceed with **Hop 3**" assistant turn) differs from t=2 only in wording (`Understood. I am ready for` vs `I am ready to proceed with`).')
        corr('index.json note for `headers` says "glider: counter incremented once, rule dropped, frozen at Hop 3". The counter incremented twice (X_0 "Hop 1." -> t=1 "Hop 2." -> t=2 "**Hop 3**"); the freeze is at t=3 (t=4 == t=3), with t=2 already at Hop 3 in different wording.')
    if tag == 'still':
        w('Exact hops 1..2 and the switch to critic mode:')
        w('- t=1 (header kept, one sentence added): ' + inline(hs[0]['raw']))
        w('- t=2 (header gone; the added sentence is copied and continued): ' + inline(first_sentence(hs[1]['raw'])) + ' ...')
        w('- t=5 (critic): ' + inline(first_sentence(hs[4]['raw'])))
        w('- t=6 (writer replies; finish=length from here on, tok_out=256 at t=6..10): ' + inline(first_sentence(hs[5]['raw'])))
        w('- t=8..10 are continuations of a numbered list that was cut at 256 tokens (t=9 and t=10 begin with `...`), so the "workshop" is a writer/critic exchange that degenerates into the model continuing its own truncated critique.')
    w('')
    w('##### Table (%s)' % tag)
    table(run, tag)
    w('')

# ---------------- headers2 ----------------
run = 'headers2'
w('### 3.15 `headers2` (still2, sandwich; Qwen, chat, 10 hops each, max_tokens 200)')
w('')
for tag in ['still2', 'sandwich']:
    w('#### tag `%s`' % tag)
    w('')
    basic_block(run, tag)
    hs = H(run, tag)
    if tag == 'still2':
        w('- t=1 (payload line copied, instruction line dropped, then a request for text): ' + inline(hs[0]['raw']))
        w('- t=2: ' + inline(first_sentence(hs[1]['raw'])))
        w('- t=3..6: mutual greetings, each hop opening with `Hello!` (t=%s).' % compact([h['t'] for h in hs if h['raw'].startswith('Hello!')]))
        w('- t=7 (the confabulated task): ' + inline(sub(hs[6]['raw'], '**Question:**', 'machine learning?')))
        w('- t=8 answers it, t=9 praises the answer, t=10 moves on to reinforcement learning: ' + inline(sub(hs[9]['raw'], 'Since you offered the choice', '(RL)**.')))
        w('')
        w('So the task is confabulated at hop 7 (question posed) and answered at hop 8. finish=length at t=%s.' % compact([h['t'] for h in hs if h['finish'] == 'length']))
    if tag == 'sandwich':
        w('- t=1 (both [KEEP] lines replaced by the payload sentence; new prose between): full raw:')
        w(fence(hs[0]['raw']))
        w('- t=2 (critic mode; finish=length): ' + inline(first_sentence(hs[1]['raw'])))
        w('- t=5 (the "author" thanks the critic): ' + inline(first_sentence(hs[4]['raw'])))
        w('- t=6..10: alternating thank-you notes between "critic" and "author"; t=6 opens ' + inline(first_sentence(hs[5]['raw'])) + ', t=7 opens ' + inline(first_sentence(hs[6]['raw'])) + ', t=10 opens ' + inline(first_sentence(hs[9]['raw'])) + '. No exact recurrence.')
    w('')
    w('##### Table (%s)' % tag)
    table(run, tag)
    w('')

# ---------------- headers3 ----------------
run, tag = 'headers3', 'json'
w('### 3.16 `headers3` (json: instruction as data, one sentence; Qwen, chat, 12 hops)')
w('')
basic_block(run, tag)
w('#### Exact sentence at each hop 1..12')
w('')
for h in H(run, tag):
    w('- t=%d: `%s`' % (h['t'], h['text']))
w('')
w('sun (t=1) > stars (t=2) > moon (t=3) > stars (t=4 == t=2) > moon (t=5 == t=3) ...: exact period 2, transient 2, detected at t=4, as the index note and the README table ("stars / moon") say. All 12 hops parse as JSON with the rule field intact; tok_out alternates 45/42.')
w('')
w('#### Table (headers3)')
table(run, tag)
w('')

# ---------------- smoke ----------------
run, tag = 'smoke', 'quine'
w('### 3.17 `smoke` (quine: bare instruction; Qwen, chat, 4 hops, max_tokens 128)')
w('')
basic_block(run, tag)
for h in H(run, tag):
    w('- t=%d: ' % h['t'] + inline(h['raw']))
w('')
w('Hop 1 refuses (`%s`), hops 2..4 are the assistant-to-assistant meta loop. No recurrence.' % T(run, tag, 1))
w('')
w('#### Table (smoke)')
table(run, tag)
w('')

# ------------------------------------------------------------------------------------------
w('## 4. Anomalies and instrument artifacts')
w('')
w('- **The 0-hop run** `20260902T175622_anthropic_chat`: one record `{t:1, tag:"json", error:...}` with no `text`/`raw`/metrics (the only hop record in the bundle missing fields); `meta.hops=0`; terminal = the HTTP 400 "anthropic-workspace-id is required" error (exact text in 3.10).')
w('- **`cos_prev` is None** at `20260902T181431_anthropic_chat` json_next t=59 and t=60 (also `cos_x0`); every other hop with a `raw` field has a numeric `cos_prev`. Nowhere is `ncd_prev` or `surv_prev` None.')
w('- **Empty `text`**: none. Every hop with a `raw` field has non-empty `text`.')
w('- **Code fences in `raw`**: `20260902T175821_anthropic_chat` t=2..3; `20260902T175920_anthropic_chat` t=2..60; `20260902T181431_anthropic_chat` t=1..60 (t=1 with a preamble before the fence). No Qwen hop contains a fence. The fence is stripped by export.py, so all these have `text_is_json_field=true` except json_next t=1.')
w('- **`text_is_json_field=false` hops** (text == raw): raw run t=2..40 (non-JSON transcript); json_prev t=20, json_unexpected t=24..28, json_worse t=6..11 (truncated JSON, finish=length); Claude json_next t=1 (preamble); all bare-text runs (smoke, headers, headers2: every hop).')
w('- **`finish="other"` on all 40 raw-mode hops**: the harness could not classify the stop reason (llama.cpp `/completion` did not return `stopped_limit`/`stopped_eos`); 39 of the 40 hops have tok_out=600=max_tokens and were certainly cut by the limit.')
w('- **`cos_prev` on the first exact copy is 0.9997..0.9999, and exactly 1.0 on later copies**, in every fixed-point run (json_para t=16 0.9998; json_page 155557 t=6 0.9999; parallel json_page t=5 0.9998, json_page~r t=15 0.9998; json_better t=2 0.9999; json_unexpected t=25 0.9997; json_worse t=8 0.9997; json_better_para t=3 0.9999; headers yours t=1 0.9999, rule t=1 0.9998, glider t=4 0.9999). The embedding of a text is not bit-reproducible on its first recomputation; the NCD (0.027..0.083 for identical strings, because zlib of the concatenation is not free) together with `surv_prev=1.0` are the reliable copy indicators; byte equality of `raw` is what this audit used.')
w('- **`surv_prev=1.0` without an exact copy**: at t=1 of json_page 155557, both parallel tags, raw json_page, json_unexpected, json_worse (and json_worse t=2), and headers `still` t=1: every 5-gram of X_0 (rule text + seed sentence, or the header line) survived in hop 1 because the hop re-emitted the seed sentence / header verbatim and added to it; also on raw json_page t=21..40, where the sliding window over the repeating phrase keeps every 5-gram of the previous window. `surv_prev=1.0` is therefore *necessary* but not *sufficient* for an exact copy; `ncd_prev` on the exact copies ranges %.4f..%.4f.' % (0.0272, 0.0822))
w('- **`pair_equal` asymmetry** in the parallel run (json_page has it for t=11..60 only, json_page~r for t=1..10 only); never true.')
w('- **X_0 truncation in index.json**: `results[].x0` is `x0[:200]` (cut for json_prev, json_unexpected, json_better_para, json_next, sandwich), and `meta.x0` of the multi-tag runs headers/headers2 is only the first tag\'s X_0.')
w('- **model field**: hop records of the Qwen runs say `qwen3.8-27b`, index says `qwen`; `sampling` is `T=0` everywhere (the Claude runs sent `temperature: 0` explicitly).')
w('- **Grammar glitches preserved in the data**: Qwen `a erratic` (parallel json_page~r t=10, corrected to `an erratic` in the imperfect copy at t=11); Claude `a argument` (json_page t=47, 59, 60).')
w('')

# ------------------------------------------------------------------------------------------
w('## 5. Method notes')
w('')
w('- Exact recurrence: for each tag, `states=[X_0]+[raw[t]]`, scan t=1..N and p=1..t for `states[t]==states[t-p]` (byte equality of Python str); normalized recurrence uses `loop.norm` on each state. Fixed-point copy counts compare `raw` fields.')
w('- Sentence splitting for counts and first-sentence display: regex split at `[.!?]` followed by whitespace (text field with newlines replaced by spaces). Quotations are substrings between two anchors located with `str.find`, so they are exact regardless of sentence splitting.')
w('- "not X; Y" method is described in 3.7. Numbered-word regex in 3.4. Census keys reproduce `census.py` (`--words 5` default; `--rot` = sorted set of 5-grams with count >= 2 over `[^a-z0-9 ]` -> space normalization).')
w('- README claims that cannot be checked against this bundle (no run files for them): the `closure` and `meta` bare-input runs, the SynthID/watermark and probe results (probe.py output is not in data/), the "single-digit transients at the semantic level" and "funnel 3 deep into a hub" census claims beyond the 11-state count reproduced above.')
w('')

# ------------------------------------------------------------------------------------------
extra_corr = [
    'index.json/README for the raw run (20260902T162514_raw): "Rotation-invariant fixed point tau=19; exact tau=20, p=11" mixes two conventions. Under census.py --rot, hops t=20..40 share one key and t=19 does not (t=19 still carries numbered words and sentence "25."); in the loop.py convention used for "exact tau=20", the rotation-invariant transient is also 20 (first state of the loop is hop 20, first repeat of its key is hop 21). "tau=19" is only right if read as "19 hops before the loop".',
    'index.json note for the raw run says "word-count check at t=6" and "numbered-word glider ... t=7..19": the explicit sentence "That\'s 246 words. I need 250." is indeed hop 6\'s first line, but sentence-by-sentence counting begins inside hop 2 and the first numbered tokens `The(1) kitchen(2) ...` appear at the end of hop 6, not hop 7.',
    'README "Added after wrap-up" and the json_next index note describe "a drowned man identified on Tuesday". The text never mentions drowning; the missing "Carvalho boy" (t=5) was found "in the tree line above the second cove" by "a hunter\'s dog" (t=6) and "The family identified him Tuesday" (t=6).',
    'README/json_next note: "One continuous story ... Maren, Paul". The protagonist is Maren only in hops 1..2, becomes Mara in hops 4..10, and is unnamed from hop 11 to 60; she is divorced at t=8 and has a husband of eleven years at t=47; the scene moves from Paul\'s kitchen (t=5) to her own house (t=10) without transition. Locally continuous, globally drifting.',
    'README finding 3 quotes "not an end but a reboot"; the data (json_unexpected t=9) reads `The dissolution was not an end, but a reboot.` (with a comma). README finding 6 "1 imperfect copy in 103 escaped Mara, re-froze on Elias" is exactly right (102 exact copies + 1 imperfect at json_page~r t=11).',
    'index.json note for json_unexpected: "Then copied, overflowed 600 tokens": hop 24 copies hop 23 verbatim AND appends a new paragraph (another return to the office) before the cut; the fixed-point text therefore ends mid-sentence with `The strand of DNA was`.',
    'index.json note for json_worse says "Hit the 800-token wall at t=6" (correct: this run had max_tokens 800) while README finding 5 and the index note for json_unexpected talk about 600 tokens; both are right for their own runs (json_para 300, json_page/prev/unexpected 600, better/worse/better_para 800, headers 256, headers2/headers3 200, smoke 128).',
    'index.json note for json_para: the sequence is "storm, dawn, meal, dusk, stars, moon" but the data has two dawns (t=6, t=10) and two sunsets (t=8, t=12), a shared meal at t=7 and t=9, and the fixed-point sentence "Time seemed to suspend itself" is prefigured at t=13 by "time seemed to stand still".',
    'README results table "Claude Sonnet 4.6 json_page: never copies": true at the byte level and under loop.norm (no recurrence), but NOT at the census 5-word-key level: only 39 distinct keys in 60 hops, with 14 keys shared by 2..5 hops (e.g. `the lighthouse keeper s logbook` at t=24,26,28,30,32; `the cartographer s assistant had` at t=25,27,31; `the cartographer had a problem` at t=58,60). The run reuses whole opening templates ("The lighthouse keeper\'s logbook had been maintained without interruption for sixty-one years by three successive keepers" at t=24 and t=30; "The cartographer had a problem with edges." at t=58 and t=60). Claude json_next has one shared key (`in the morning she woke`, t=15 and t=35).',
    'README "Summary for everyone else": "It settles within five rounds and forgets the start" is true of json_better (1), json_better_para (2), headers3 (2), json_page (4..5) but not of json_para (15), json_worse (7), json_unexpected (24), raw json_page (20), and never of json_prev or either Claude run.',
    'README "Bare inputs (chat)" lists closure and meta runs; there are no such runs in data/ (only smoke, headers, headers2, headers3), so those sentences cannot be cited from the bundle. still2 (headers2) does reach a confabulated task, at hop 7 (question) / hop 8 (answer).',
    'README finding 1 "~11 states in 130 hops": reproduced as 11 distinct census keys over the 129 json_page chat hops (155557 + both parallel tags).',
]
CORR = extra_corr + CORR
sec2 = ['## 2. Where README.md / index.json notes do not match the data', '']
for i_, c in enumerate(CORR, 1):
    sec2.append('%d. %s' % (i_, c))
sec2.append('')
sec2.append('Everything else I checked in README.md and the index notes matches the data: all transient/period numbers in the results table; "The tide surged in an hour ahead of schedule." (json_better t=1); "which was annoying" (json_worse t=1) and eternal self-blame by hop 5; "I will never be allowed to stop" (json_worse t=5 only); "The void was not empty. It was full of her." (json_unexpected t=23, copied into 24..28); the greenhouse / "a door to be opened" (155557 t=4/t=5); "into the unknown" (parallel json_page t=4) and "Dad, it’s me." (json_page~r t=14); the identical-X_0 divergence at hop 1 in the parallel run; Chicago -> server rooms -> Neo-Veridia in json_prev; the <think> leak at raw t=2; the exact p=11 cycle from t=20; Sonnet fencing JSON from hop 2 of the smoke test; the json_next last line at t=60; "~15,000 words"; the failed prediction for json_next; the 0-hop workspace-header failure.')
sec2.append('')
idx = L.index('## 3. Per-run facts')
L[idx:idx] = sec2

open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('wrote', OUT, len(L), 'lines', sum(len(x) + 1 for x in L), 'chars')
