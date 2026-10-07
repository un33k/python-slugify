import csv, os, sys
res = sys.argv[1]
print("\n| Condition | Passed | Avg turns | Avg cost (USD) | Hook blocks |\n|---|---|---|---|---|")
for name in ("baseline", "harness"):
    p = os.path.join(res, name + ".csv")
    if not os.path.exists(p): continue
    rows = list(csv.DictReader(open(p)))
    n = len(rows); ok = sum(r["pass"] == "pass" for r in rows)
    t = [float(r["turns"]) for r in rows if r["turns"]]
    c = [float(r["cost_usd"]) for r in rows if r["cost_usd"]]
    log = os.path.join(res, f"hook_blocks_{name}.log")
    blocks = sum(1 for _ in open(log)) if os.path.exists(log) else 0
    print(f"| {name} ({n} runs) | {ok}/{n} | {sum(t)/len(t):.1f} | {sum(c)/len(c):.3f} | {blocks} |" if t and c
          else f"| {name} ({n} runs) | {ok}/{n} | n/a | n/a | {blocks} |")
print()
