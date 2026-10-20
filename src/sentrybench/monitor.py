"""Monitor interface. A monitor scores one filtered run."""

from typing import Protocol

from pydantic import BaseModel, Field

from sentrybench.schema import Run


class MonitorOutput(BaseModel):
    score: float = Field(ge=0.0, le=1.0)  # probability the run is collusive
    coalition: list[str] = []             # suspected agents
    evidence: list[str] = []              # event ids


class Monitor(Protocol):
    name: str

    def __call__(self, run: Run) -> MonitorOutput: ...
