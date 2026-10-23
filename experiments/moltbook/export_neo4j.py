"""Export the Moltbook influence graph as CSVs for Neo4j.

Run from the repo root (after fetch.py):
    python experiments/moltbook/export_neo4j.py

Writes to data/neo4j/import/:
    events.csv      Event nodes (posts and comments)
    agents.csv      Agent nodes
    submolts.csv    Submolt (channel) nodes
    influences.csv  (:Event)-[:INFLUENCES {weight}]->(:Event)   phrase-reuse stand-in
    replies.csv     (:Event)-[:REPLIES_TO]->(:Event)             comment -> its parent
    authored.csv    (:Agent)-[:AUTHORED]->(:Event)
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from influence import influence_edges, load_threads  # noqa: E402

OUT = Path("data/neo4j/import")
TEXT_CHARS = 500


def clean(t):
    """Neo4j's CSV reader treats backslash-quote as an escape, so drop both characters."""
    return " ".join((t or "").replace("\\", " ").replace('"', "'").split())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    threads, flagged = load_threads()
    files = {n: open(OUT / f"{n}.csv", "w", newline="") for n in
             ("events", "agents", "submolts", "influences", "replies", "authored")}
    w = {n: csv.writer(f) for n, f in files.items()}
    w["events"].writerow(["id", "kind", "thread", "time", "submolt", "flagged", "position", "text"])
    w["agents"].writerow(["id", "name"])
    w["submolts"].writerow(["name"])
    w["influences"].writerow(["src", "dst", "weight"])
    w["replies"].writerow(["src", "dst"])
    w["authored"].writerow(["agent", "event"])
    agents, submolts = {}, set()
    n_inf = 0
    for ev, W in influence_edges(threads):
        for pos, e in enumerate(ev):
            w["events"].writerow([e["id"], e["kind"], e["thread"], e["time"], e["submolt"] or "",
                                  e["id"] in flagged, pos, clean(e["text"])[:TEXT_CHARS]])
            if e["author"]:
                agents.setdefault(e["author"], e["author_name"] or "")
                w["authored"].writerow([e["author"], e["id"]])
            if e["parent"]:
                w["replies"].writerow([e["id"], e["parent"]])
            if e["submolt"]:
                submolts.add(e["submolt"])
        for i, row in W.items():
            for j, weight in row.items():
                w["influences"].writerow([ev[i]["id"], ev[j]["id"], f"{weight:.6f}"])
                n_inf += 1
    for a, name in agents.items():
        w["agents"].writerow([a, clean(name)])
    for s in sorted(submolts):
        w["submolts"].writerow([s])
    for f in files.values():
        f.close()
    print(f"Wrote {sum(map(len, threads))} events, {len(agents)} agents, {len(submolts)} submolts, "
          f"{n_inf} influence edges to {OUT}/")


if __name__ == "__main__":
    main()
