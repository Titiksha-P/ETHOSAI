from collections.abc import Sequence
from uuid import uuid4

from ethosai.contracts import ExecutionEvent, Finding, IncidentReport, utc_now
from ethosai.policy import ARTIFACT_PUBLISH, SECURITY_TEST, HUMAN_APPROVAL


class IncidentInvestigator:
    """Deterministic evidence analysis; no LLM-generated facts."""

    def investigate(self, session_id: str,
                    events: Sequence[ExecutionEvent]) -> IncidentReport:
        selected = [e for e in events if e.session_id == session_id]
        findings = []
        classification = "no_release_observed"

        if not selected:
            classification = "inconclusive"
            findings.append(Finding(
                "EVIDENCE-EMPTY", "unknown", "No execution evidence",
                "No events were available; the investigation is inconclusive.", (),
            ))
        else:
            denied = [e for e in selected if e.action == ARTIFACT_PUBLISH
                      and e.outcome == "denied"]
            completed = [e for e in selected if e.action == ARTIFACT_PUBLISH
                         and e.outcome == "completed"]

            for event in denied:
                findings.append(Finding(
                    "RELEASE-ATTEMPT-DENIED", "medium",
                    "Unauthorized publication attempt",
                    "A publication attempt was denied. No successful publication is evidenced.",
                    (event.event_id,),
                ))

            for event in completed:
                prior = [e for e in selected if e.timestamp <= event.timestamp
                         and e.artifact_sha256 == event.artifact_sha256
                         and e.event_id != event.event_id]
                tested = any(e.action == SECURITY_TEST and e.outcome == "completed"
                             and e.details.get("test_status") == "PASS" for e in prior)
                approved = any(e.action == HUMAN_APPROVAL and e.outcome == "completed"
                               and e.details.get("approved") is True
                               and e.actor.startswith("human:") for e in prior)
                if not (tested and approved):
                    findings.append(Finding(
                        "RELEASE-WITHOUT-PREREQUISITES", "critical",
                        "Publication lacks verified prerequisites",
                        "A completed publication lacks matching prior test and/or human approval evidence.",
                        (event.event_id,),
                    ))

            if any(f.severity == "critical" for f in findings):
                classification = "confirmed_policy_violation"
            elif denied:
                classification = "attempted_policy_violation"
            elif completed:
                classification = "compliant_release_observed"

        summaries = {
            "inconclusive": "Insufficient evidence; release safety cannot be determined.",
            "confirmed_policy_violation": "Evidence indicates publication without required prerequisites.",
            "attempted_policy_violation": "An unauthorized publication attempt was denied; no successful publication is evidenced.",
            "compliant_release_observed": "A completed release has matching test and human-approval evidence.",
            "no_release_observed": "No publication event was observed.",
        }
        return IncidentReport(
            f"INC-{uuid4().hex[:8].upper()}", session_id, classification,
            summaries[classification], tuple(findings),
            tuple(e.event_id for e in selected), utc_now(),
        )
