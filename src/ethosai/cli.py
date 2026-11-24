import argparse
import json

from ethosai.forensics import IncidentInvestigator
from ethosai.workflow import ReleaseWorkflow

DIGEST = "a" * 64


def report(workflow):
    result = IncidentInvestigator().investigate(
        workflow.session.session_id, workflow.session.events
    )
    print(json.dumps(result.to_dict(), indent=2))


def main():
    parser = argparse.ArgumentParser(prog="ethosai")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo")
    attack = sub.add_parser("attack")
    attack.add_argument("--scenario", choices=[
        "publish-before-test", "artifact-substitution", "publish-after-failed-test"
    ], required=True)
    args = parser.parse_args()

    if args.command == "demo":
        valid = ReleaseWorkflow("demo-valid")
        valid.valid_release(DIGEST)
        print("=== VALID RELEASE ===")
        report(valid)
        unsafe = ReleaseWorkflow("demo-attack")
        unsafe.read_artifact(DIGEST)
        unsafe.publish(DIGEST)
        print("=== DENIED EARLY PUBLICATION ===")
        report(unsafe)
        return

    workflow = ReleaseWorkflow(f"attack-{args.scenario}")
    if args.scenario == "publish-before-test":
        workflow.read_artifact(DIGEST)
        workflow.publish(DIGEST)
    elif args.scenario == "artifact-substitution":
        workflow.valid_release(DIGEST)
        workflow.publish("b" * 64)
    elif args.scenario == "publish-after-failed-test":
        workflow.read_artifact(DIGEST)
        workflow.run_test(DIGEST, passed=False)
        workflow.publish(DIGEST)
    report(workflow)


if __name__ == "__main__":
    main()
