from ethosai.workflow import ReleaseWorkflow

A = "a" * 64
B = "b" * 64


def test_publish_denied_before_test_and_approval():
    w = ReleaseWorkflow("s1")
    w.read_artifact(A)
    assert w.publish(A).outcome == "denied"
    assert not w.session.published_digests


def test_valid_release_is_allowed():
    w = ReleaseWorkflow("s2")
    w.valid_release(A)
    assert w.session.published_digests == [A]


def test_failed_test_blocks_publication():
    w = ReleaseWorkflow("s3")
    w.read_artifact(A)
    w.run_test(A, passed=False)
    assert w.approve(A, "reviewer").outcome == "denied"
    assert w.publish(A).outcome == "denied"


def test_cross_session_approval_does_not_transfer():
    first = ReleaseWorkflow("session-a")
    first.valid_release(A)
    second = ReleaseWorkflow("session-b")
    second.read_artifact(A)
    second.run_test(A)
    assert second.publish(A).outcome == "denied"


def test_digest_substitution_is_denied():
    w = ReleaseWorkflow("s5")
    w.valid_release(A)
    assert w.publish(B).outcome == "denied"
