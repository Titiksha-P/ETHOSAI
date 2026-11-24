from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ExecutionEvent:
    session_id: str
    action: str
    artifact_sha256: str
    outcome: str
    actor: str
    timestamp: str
    event_id: str
    details: dict[str, Any]

    @classmethod
    def create(cls, *, session_id: str, action: str, artifact_sha256: str,
               outcome: str, actor: str, details: dict[str, Any] | None = None):
        return cls(session_id, action, artifact_sha256, outcome, actor,
                   utc_now(), str(uuid4()), details or {})

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    title: str
    description: str
    evidence_event_ids: tuple[str, ...]


@dataclass(frozen=True)
class IncidentReport:
    incident_id: str
    session_id: str
    classification: str
    summary: str
    findings: tuple[Finding, ...]
    evidence_event_ids: tuple[str, ...]
    generated_at: str

    def to_dict(self):
        return {
            "incident_id": self.incident_id,
            "session_id": self.session_id,
            "classification": self.classification,
            "summary": self.summary,
            "findings": [asdict(f) for f in self.findings],
            "evidence_event_ids": list(self.evidence_event_ids),
            "generated_at": self.generated_at,
        }
