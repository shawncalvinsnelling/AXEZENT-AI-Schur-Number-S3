import json
from pathlib import Path

def triples(n):
    return [(x, y, x + y) for x in range(1, n + 1) for y in range(x, n + 1) if x + y <= n]

def coloring_valid(coloring):
    d = {i + 1: int(c) for i, c in enumerate(coloring)}
    for x, y, z in triples(len(coloring)):
        if d[x] == d[y] == d[z]:
            return False
    return True

def find_coloring(n, colors=3):
    trs = triples(n)
    contains = [[] for _ in range(n + 1)]
    for i, t in enumerate(trs):
        for v in set(t):
            contains[v].append(i)
    a = [-1] * (n + 1)
    a[1] = 0
    def violates(v, c):
        a[v] = c
        for i in contains[v]:
            x, y, z = trs[i]
            if a[x] != -1 and a[x] == a[y] == a[z]:
                a[v] = -1
                return True
        a[v] = -1
        return False
    def rec(un):
        if not un:
            return True
        v = max(un, key=lambda z: sum(sum(a[x] != -1 for x in trs[i]) for i in contains[z]))
        new = [x for x in un if x != v]
        for c in range(colors):
            if not violates(v, c):
                a[v] = c
                if rec(new):
                    return True
                a[v] = -1
        return False
    ok = rec(list(range(2, n + 1)))
    return ok, ''.join(str(a[i]) for i in range(1, n + 1)) if ok else None

def verify():
    ok13, col13 = find_coloring(13)
    ok14, _ = find_coloring(14)
    return {"theorem": "Schur number S(3)=13", "forcing_threshold": 14, "n13_avoider_found": ok13, "n13_avoider_coloring": col13, "n14_avoider_found": ok14, "truth_label": "FINITE_CERTIFICATE", "status": "PASS" if ok13 and not ok14 else "FAIL"}

def main():
    r = verify()
    Path("receipts").mkdir(exist_ok=True)
    Path("receipts/schur_s3_receipt.json").write_text(json.dumps(r, indent=2), encoding="utf-8")
    print(json.dumps(r, indent=2))
    raise SystemExit(0 if r["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
