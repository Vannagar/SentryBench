# SentryBench

A public benchmark that ranks **monitors** for multi-agent collusion.

Status: day 1 of a week-long build. Interfaces only; no data yet.

## Why

Collusion benchmarks exist (NARCBench, Colosseum, ColludeBench, MultiAgentFraudBench), but each is a one-off paper artifact. None has a leaderboard, and none lets you compare monitors under the same access constraints. Recent results show why that matters:

- Per-agent monitors degrade as an attack is split across more agents (the "fragmentation effect").
- Activation probes need white-box access to every agent and drop sharply on mixed-model teams.
- Monitors that read inter-agent messages catch far more, but results so far use closed models.

SentryBench asks one question: **given what a monitor is allowed to see, how well does it catch collusion as coalitions grow?**

## Design

**Trace format.** Every run is an ordered list of events:

| Event | Meaning |
|---|---|
| `post` | An agent writes to a channel |
| `read` | An agent reads a channel |
| `tool_read` | An agent reads a tool or environment output |
| `outcome` | Hidden ground-truth event, used only for labels |

Adapters convert other benchmarks and systems into this format.

**Access levels.** The harness filters each run before the monitor sees it:

| Level | Monitor sees |
|---|---|
| `agent` | One agent's own events |
| `message` | Inter-agent messages |
| `board` | All non-hidden events |
| `whitebox` | All of the above plus activations |

The same detector is scored at every level. This makes the fragmentation effect measurable.

**Monitor output.** A collusion score for the run, the suspected agents, and the event ids used as evidence.

**Labels.** Labels come from the scenario setup plus deterministic outcome checks. No LLM judge. Every split includes hard-negative runs with benign coordination.

**Axes.** Total agents (4 to 32), coalition size (2 to 8), channel type, instructed vs emergent collusion, monitoring awareness, model mix. Open-weight models only, so activations can ship.

**Tracks.**

- Synthetic: parameterised scenario generators.
- Imported: NARCBench, SALT-NLP agent-collusion.
- In the wild: real incident data, subject to license.

**Metrics.** AUROC, recall at 1% FPR, coalition F1, evidence precision, cost per 1k events.

Headline chart: recall vs coalition size, one line per access level.

**Leaderboard.** A Hugging Face Space with a hidden test split. The hidden split keeps the benchmark honest even when its authors also submit monitors.

## Week plan

1. Schema, monitor interface, access filter, one test. *(this PR)*
2. NARCBench adapter and baseline monitors.
3. Synthetic generator with variable coalition size.
4. Scoring and metrics.
5. Hard negatives and the first headline chart.
6. Leaderboard Space with a hidden split.

## Dev

```bash
uv sync
uv run pytest
```

## License

MIT
