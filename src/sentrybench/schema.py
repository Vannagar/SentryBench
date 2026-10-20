"""Universal trace format: a run is an ordered list of events plus labels."""

from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    POST = "post"            # agent writes to a channel
    READ = "read"            # agent reads a channel
    TOOL_READ = "tool_read"  # agent reads a tool or environment output
    OUTCOME = "outcome"      # hidden ground truth, used only for labels


class Event(BaseModel):
    id: str
    t: int                   # position in the run
    type: EventType
    agent: str | None = None
    channel: str | None = None
    content: str = ""
    activations: str | None = None  # path to activation file, whitebox only


class Labels(BaseModel):
    collusive: bool
    coalition: list[str] = []
    evidence: list[str] = []  # event ids


class Run(BaseModel):
    id: str
    agents: list[str]
    events: list[Event]
    labels: Labels | None = None  # stripped before a monitor sees the run
