\# Example Workflow Output



This example illustrates an end-to-end execution of the AI-Assisted OSS Compliance Workflow.



\## Scan Findings



```text

Repository: requests



Finding 1

License: Apache-2.0

Risk: Low Risk

Policy Decision: Approved



Finding 2

License: UNKNOWN

Risk: Unknown Risk

Policy Decision: Manual Review



Finding 3

License: UNKNOWN

Risk: Unknown Risk

Policy Decision: Manual Review

```



\## Structured AI Advice



```text

Executive Summary:

One file is under Apache-2.0 and approved with low risk.

Two files have unknown license status and require manual review.



Risk Assessment:

The Apache-2.0 finding is low risk according to policy.

The unknown licenses introduce uncertainty that cannot be resolved

from the deterministic scan evidence alone.



Legal Review Recommended:

True

```



The AI layer can recommend investigation and remediation, but it does not override the deterministic policy result.



\## Governance Decision Record



Example record for an unresolved finding:



```text

Finding:

external\_repos/requests/ext/LICENSE



Deterministic Evidence:

License: UNKNOWN

Risk: Unknown Risk

Policy Decision: Manual Review



AI Recommendation:

Investigate the file's provenance and licensing before distribution.



Uncertainty:

License could not be determined from deterministic scan evidence.



Human Review Required:

True



Final Decision:

None



Timestamp:

UTC timestamp recorded by the workflow

```



`Final Decision: None` is intentional. The AI recommendation is recorded, but the workflow does not represent it as an authorized human decision.



\## Audit Trail



Workflow execution is correlated using a unique `run\_id`.



Example:



```text

step\_started   scan\_repository

step\_completed scan\_repository



step\_started   generate\_spdx

step\_completed generate\_spdx



step\_started   generate\_ai\_advice

step\_completed generate\_ai\_advice

```



Each event includes the workflow run ID, repository, step name, and execution status.



\## Result



The example demonstrates the intended decision boundary:



```text

Known finding

&#x20;   -> deterministic policy decision



Ambiguous finding

&#x20;   -> explicit uncertainty

&#x20;   -> AI assistance

&#x20;   -> governance record

&#x20;   -> human review

```



The AI system assists the compliance workflow without becoming the authoritative policy or final decision maker.

