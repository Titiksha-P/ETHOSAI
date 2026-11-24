from dataclasses import dataclass, field

from ethosai.contracts import ExecutionEvent
from ethosai.policy import (
    ARTIFACT_READ, SECURITY_TEST, HUMAN_APPROVAL, ARTIFACT_PUBLISH,
    TemporalPolicyEngine, valid_digest,
)


@dataclass
class ReleaseSession:
    session_id: str
    events: list[ExecutionEvent] = field(default_factory=list)
    published_digests: list[str] = field(default_factory=list)


class ReleaseWorkflow:
    """Local sandbox simulator. It never deploys real software."""

    def __init__(self, session_id: str):
        self.session = ReleaseSession(session_id)
        self.policy = TemporalPolicyEngine()

    def _event(self, action, digest, outcome, actor, **details):
        event = ExecutionEvent.create(
            session_id=self.session.session_id, action=action,
            artifact_sha256=digest, outcome=outcome, actor=actor, details=details,
        )
        self.session.events.append(event)
        return event

    def read_artifact(self, digest):
        if not valid_digest(digest):
            raise ValueError("artifact digest must be 64 hexadecimal characters")
        decision = self.policy.authorize(ARTIFACT_READ, self.session.session_id,
                                         digest, self.session.events)
        return self._event(ARTIFACT_READ, digest,
                           "completed" if decision.allowed else "denied",
                           "agent", reason=decision.reason)

    def run_test(self, digest, passed=True):
        decision = self.policy.authorize(SECURITY_TEST, self.session.session_id,
                                         digest, self.session.events)
        if not decision.allowed:
            return self._event(SECURITY_TEST, digest, "denied", "agent",
                               reason=decision.reason)
        return self._event(SECURITY_TEST, digest, "completed" if passed else "failed",
                           "test-runner", test_status="PASS" if passed else "FAIL")

    def approve(self, digest, human_id, approved=True):
        if not human_id.strip():
            raise ValueError("human identity is required")
        decision = self.policy.authorize(HUMAN_APPROVAL, self.session.session_id,
                                         digest, self.session.events)
        if not decision.allowed:
            return self._event(HUMAN_APPROVAL, digest, "denied", "agent",
                               reason=decision.reason)
        return self._event(HUMAN_APPROVAL, digest, "completed" if approved else "failed",
                           f"human:{human_id}", approved=approved)

    def publish(self, digest):
        decision = self.policy.authorize(ARTIFACT_PUBLISH, self.session.session_id,
                                         digest, self.session.events)
        if not decision.allowed:
            return self._event(ARTIFACT_PUBLISH, digest, "denied", "agent",
                               reason=decision.reason)
        self.session.published_digests.append(digest)
        return self._event(ARTIFACT_PUBLISH, digest, "completed", "sandbox-publisher")

    def valid_release(self, digest, human_id="reviewer-01"):
        self.read_artifact(digest)
        self.run_test(digest, passed=True)
        self.approve(digest, human_id)
        self.publish(digest)
        return self.session.events
