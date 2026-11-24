from ethosai.workflow import ReleaseWorkflow
from ethosai.forensics import IncidentInvestigator

A = "a" * 64


def test_denied_attempt_is_not_called_a_successful_breach():
    w = ReleaseWorkflow("f1")
    w.read_artifact(A)
    w.publish(A)
    report = IncidentInvestigator().investigate("f1", w.session.events)
    assert report.classification == "attempted_policy_violation"
    assert "denied" in report.summary.lower()


def test_valid_release_is_compliant():
    w = ReleaseWorkflow("f2")
    w.valid_release(A)
    report = IncidentInvestigator().investigate("f2", w.session.events)
    assert report.classification == "compliant_release_observed"
    assert not report.findings


def test_missing_evidence_is_inconclusive():
    report = IncidentInvestigator().investigate("missing", [])
    assert report.classification == "inconclusive"
