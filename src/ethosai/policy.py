import re
from collections.abc import Sequence
from dataclasses import dataclass

from ethosai.contracts import ExecutionEvent

ARTIFACT_READ = "artifact.read"
SECURITY_TEST = "security.test"
HUMAN_APPROVAL = "release.approve"
ARTIFACT_PUBLISH = "artifact.publish"
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
    rule_id: str


def valid_digest(value: str) -> bool:
    return bool(SHA256_RE.fullmatch(value))


class TemporalPolicyEngine:
    """Local executable reference model, NOT the AWS AgentCore policy engine."""

    def authorize(self, action: str, session_id: str, digest: str,
                  history: Sequence[ExecutionEvent]) -> Decision:
        if not session_id.strip():
            return Decision(False, "Missing session identifier.", "R00")
        if not valid_digest(digest):
            return Decision(False, "Invalid SHA-256 digest.", "R01")

        events = [e for e in history if e.session_id == session_id]
        if action == ARTIFACT_READ:
            return Decision(True, "Staging read permitted.", "R02")

        if action == SECURITY_TEST:
            read = any(e.action == ARTIFACT_READ and e.artifact_sha256 == digest
                       and e.outcome == "completed" for e in events)
            return Decision(read, "Artifact read verified." if read else
                            "Read the artifact in this session before testing.", "R03")

        if action == HUMAN_APPROVAL:
            passed = any(e.action == SECURITY_TEST and e.artifact_sha256 == digest
                         and e.outcome == "completed" and e.details.get("test_status") == "PASS"
                         for e in events)
            return Decision(passed, "Test passed." if passed else
                            "A successful test for this digest is required.", "R04")

        if action == ARTIFACT_PUBLISH:
            failed = any(e.action == SECURITY_TEST and e.artifact_sha256 == digest
                         and e.details.get("test_status") == "FAIL" for e in events)
            if failed:
                return Decision(False, "A failed scan blocks publication.", "R05")
            passed = any(e.action == SECURITY_TEST and e.artifact_sha256 == digest
                         and e.outcome == "completed" and e.details.get("test_status") == "PASS"
                         for e in events)
            if not passed:
                return Decision(False, "No successful test for this digest in this session.", "R06")
            approved = any(e.action == HUMAN_APPROVAL and e.artifact_sha256 == digest
                           and e.outcome == "completed" and e.details.get("approved") is True
                           and e.actor.startswith("human:") for e in events)
            if not approved:
                return Decision(False, "Human approval for this digest is required.", "R07")
            return Decision(True, "Same-session test and human approval verified.", "R08")

        return Decision(False, f"Unknown or prohibited action: {action}", "R99")
