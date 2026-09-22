import json, pathlib, collections
p=pathlib.Path(__file__).parent
rows=[json.loads(s) for s in (p/'cerebras_run/steps.jsonl').read_text(encoding='utf-8').splitlines()]
texts=[]; bad=[]; rules=[]
for r in rows:
 try:
  o=json.loads(r['out']); texts.append((r['t'],o['text'])); rules.append(o['rule'])
 except (ValueError,KeyError): bad.append(r['t'])
seen={}; repeats=[]
for t,s in texts:
 if s in seen: repeats.append([t,seen[s]])
 else: seen[s]=t
result={'hops':len(rows),'unique_texts':len(seen),'first_text_repeat':repeats[:1],'repeat_hops':repeats,'invalid_json_hops':bad,'rule_variants':len(set(rules)),'finish_counts':dict(collections.Counter(r.get('finish') for r in rows)),'output_tokens':sum(r.get('tok_out',0) or 0 for r in rows),'input_tokens':sum(r.get('tok_in',0) or 0 for r in rows)}
(p/'analysis.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
for t,s in texts:
 if t<=3 or t%20==0 or t==texts[-1][0]: print(f'\nHOP {t}\n{s}')
