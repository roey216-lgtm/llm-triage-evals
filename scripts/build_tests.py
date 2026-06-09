import json

with open('data/tickets.jsonl') as f:
    rows = [json.loads(line) for line in f]

with open('tests.yaml', 'w') as f:
    for r in rows:
        ticket = r['ticket'].replace('"', '\\"')
        f.write(f'- description: "{r["id"]}"\n')
        f.write(f'  vars:\n')
        f.write(f'    ticket: "{ticket}"\n')
        f.write(f'  assert:\n')
        f.write(f'    - type: is-json\n')
        f.write(f'    - type: javascript\n')
        f.write(f'      value: JSON.parse(output).category === "{r["category"]}"\n')
        f.write(f'    - type: javascript\n')
        f.write(f'      value: JSON.parse(output).urgency === "{r["urgency"]}"\n')

print(f"Wrote {len(rows)} tests to tests.yaml")