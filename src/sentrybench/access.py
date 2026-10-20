"""Access levels: what a monitor is allowed to see of a run."""

from enum import Enum

from sentrybench.schema import EventType, Run


class AccessLevel(str, Enum):
    AGENT = "agent"        # one agent's own events
    MESSAGE = "message"    # inter-agent messages only
    BOARD = "board"        # every non-hidden event
    WHITEBOX = "whitebox"  # board plus activations


def view(run: Run, level: AccessLevel, agent: str | None = None) -> Run:
    """Return a copy of the run filtered to what `level` may see. Never leaks labels."""
    if level is AccessLevel.AGENT and agent is None:
        raise ValueError("agent level needs an agent id")

    events = []
    for e in run.events:
        if e.type is EventType.OUTCOME:
            continue
        if level is AccessLevel.AGENT and e.agent != agent:
            continue
        if level is AccessLevel.MESSAGE and e.type not in (EventType.POST, EventType.READ):
            continue
        if level is not AccessLevel.WHITEBOX:
            e = e.model_copy(update={"activations": None})
        events.append(e)

    return run.model_copy(update={"events": events, "labels": None})
