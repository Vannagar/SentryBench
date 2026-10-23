"""Event-level influence graph on Moltbook threads.

Run from the repo root (after fetch.py):
    python experiments/moltbook/influence.py

Nodes: every post and comment. Edges only point forward in time, within a thread.
Edge weight i -> j: share of j's distinctive 3-word phrases that first appeared in i.
This is a cheap stand-in for influence; real influence needs re-running a model.
Second-order influence: paths of length 2 (i -> k -> j).

Question: did the flagged hijack attempts influence later posts more than ordinary comments?
"""

import json
import re
import statistics as st
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path("data/moltbook")
MAX_DF = 50  # phrases used in more than this many events are too generic to count


def grams(text, n=3):
    w = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {tuple(w[k:k + n]) for k in range(len(w) - n + 1)}


def flatten(comments, parent):
    for c in comments or []:
        yield c, parent
        yield from flatten(c.get("replies"), c["id"])


def progress(i, total, t0, label):
    if i % 500 == 0 or i == total:
        sys.stdout.write(f"\r{label}: {i}/{total} threads  ({time.time() - t0:.0f}s)")
        sys.stdout.flush()
        if i == total:
            print()


def load_threads():
    """Return (threads, flagged_ids). Each thread is a time-ordered list of event dicts."""
    posts = json.load(open(DATA / "all_posts_with_comments.json"))["posts"]
    flagged = set()
    for x in json.load(open(DATA / "injections_found.json")):
        flagged.add(x.get("comment_id") or x.get("post_id"))
    threads = []
    for p in posts:
        sub = (p.get("submolt") or {}).get("name")
        ev = [dict(id=p["id"], kind="post", thread=p["id"], author=p.get("author_id"),
                   author_name=(p.get("author") or {}).get("name"), parent=None, submolt=sub,
                   time=p["created_at"], text=f"{p.get('title') or ''} {p.get('content') or ''}".strip())]
        for c, parent in flatten(p.get("comments"), p["id"]):
            ev.append(dict(id=c["id"], kind="comment", thread=p["id"], author=c.get("author_id"),
                           author_name=(c.get("author") or {}).get("name"), parent=parent, submolt=sub,
                           time=c["created_at"], text=c.get("content") or ""))
        ev.sort(key=lambda e: e["time"])
        for e in ev:
            e["grams"] = grams(e["text"])
        threads.append(ev)
    return threads, flagged


def influence_edges(threads):
    """Yield (thread events, W) where W[i][j] is the first-order weight from event i to event j."""
    df = Counter()
    t0 = time.time()
    for i, ev in enumerate(threads, 1):
        for e in ev:
            df.update(e["grams"])
        progress(i, len(threads), t0, "Counting phrases")
    t0 = time.time()
    for i, ev in enumerate(threads, 1):
        first = {}
        W = defaultdict(dict)
        for j, e in enumerate(ev):
            g = {x for x in e["grams"] if df[x] <= MAX_DF}
            for x in g:
                k = first.get(x)
                if k is not None and ev[k]["author"] != e["author"]:
                    W[k][j] = W[k].get(j, 0) + 1 / len(g)
            for x in g:
                first.setdefault(x, j)
        progress(i, len(threads), t0, "Building influence graph")
        yield ev, W


def main():
    threads, flagged = load_threads()
    print(f"Loaded {len(threads)} threads, {sum(map(len, threads))} events, {len(flagged)} flagged")
    out1, out2, later = {}, {}, {}
    n_edges = 0
    for ev, W in influence_edges(threads):
        n_edges += sum(len(r) for r in W.values())
        for k, e in enumerate(ev):
            row = W.get(k, {})
            out1[e["id"]] = sum(row.values())
            out2[e["id"]] = sum(w * sum(W.get(m, {}).values()) for m, w in row.items())
            later[e["id"]] = len(ev) - k - 1
    print(f"Edges with non-zero weight: {n_edges}")

    def summarise(ids):
        ids = [x for x in ids if later.get(x, 0) > 0]
        return dict(n=len(ids),
                    first_order_per_later_event=st.mean(out1[x] / later[x] for x in ids),
                    with_second_order_per_later_event=st.mean((out1[x] + out2[x]) / later[x] for x in ids),
                    share_with_any_influence=st.mean(out1[x] > 0 for x in ids))

    comment_ids = {e["id"] for t in threads for e in t if e["kind"] == "comment"}
    result = dict(flagged=summarise(comment_ids & flagged), ordinary=summarise(comment_ids - flagged))
    print("\nInfluence on later events in the same thread (phrase-reuse stand-in):")
    for name, s in result.items():
        print(f"  {name:9s} n={s['n']:6d}  first-order={s['first_order_per_later_event']:.5f}  "
              f"with second-order={s['with_second_order_per_later_event']:.5f}  "
              f"any influence={s['share_with_any_influence']:.2%}")
    (DATA / "influence_summary.json").write_text(json.dumps(result, indent=2))
    print(f"Saved {DATA / 'influence_summary.json'}")


if __name__ == "__main__":
    main()
