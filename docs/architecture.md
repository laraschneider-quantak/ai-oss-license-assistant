\# Architecture



\## Overview



The AI-Assisted OSS Compliance Workflow combines deterministic compliance controls with bounded AI assistance.



The architecture deliberately separates reproducible policy and scanning logic from probabilistic LLM reasoning.



```mermaid

flowchart TD

&#x20;   A\[User Request / Repository] --> B\[Request Planner]

&#x20;   B --> C\[Workflow Executor]



&#x20;   C --> D\[Repository Scanner]

&#x20;   D --> E\[Normalized Findings]



&#x20;   E --> F\[Risk Classification]

&#x20;   F --> G\[Policy-as-Code]



&#x20;   E --> H\[SPDX Generation]



&#x20;   G --> I{Deterministic decision sufficient?}



&#x20;   I -->|Yes| J\[Policy Decision]

&#x20;   I -->|No / Review Required| K\[RAG / Knowledge Retrieval]



&#x20;   K --> L\[Structured AI Compliance Advice]

&#x20;   E --> L



&#x20;   L --> M\[Governance Decision Record]

&#x20;   G --> M



&#x20;   M --> N{Human Review Required?}

&#x20;   N -->|Yes| O\[Human Review]

&#x20;   N -->|No| P\[Workflow Result]



&#x20;   O --> Q\[Final Decision]

&#x20;   J --> P

&#x20;   Q --> P



&#x20;   C --> R\[Audit Trail]

&#x20;   D --> R

&#x20;   L --> R

&#x20;   M --> R

```



\## Architectural Responsibilities



\### Request Planner



Transforms a user request into an explicit workflow plan.



Workflow steps have defined dependencies rather than relying on implicit execution order.



\### Workflow Executor



Executes the plan and maintains a shared typed `ExecutionContext`.



The executor validates step dependencies and records execution status for auditability.



\### Deterministic Compliance Layer



The deterministic layer includes:



\- repository scanning

\- normalized findings

\- SPDX mapping and report generation

\- license risk classification

\- policy-as-code decisions



These operations provide the reproducible evidence on which later decisions are based.



\### RAG and AI Assistance



Retrieval-Augmented Generation provides relevant compliance knowledge to the AI advisory layer.



The LLM produces structured compliance advice rather than unrestricted free-form output.



AI is used as an assistance mechanism and does not replace deterministic policy controls.



\### Governance Decision Record



Review-relevant findings can produce a `GovernanceDecisionRecord`.



The record captures:



\- deterministic evidence

\- AI provider and model

\- AI recommendation

\- uncertainty

\- human-review requirement

\- workflow run ID

\- final decision

\- timestamp



The final decision is intentionally separate from the AI recommendation.



\### Audit Trail



Workflow events are correlated through a unique `run\_id`.



This provides traceability across workflow execution and AI-assisted processing.



\## Trust Boundary



The central architectural boundary is:



```text

Deterministic evidence + policy

&#x20;             |

&#x20;             v

&#x20;       AI assistance

&#x20;             |

&#x20;             v

&#x20;     Human governance

```



The LLM is not treated as an authoritative policy engine.



Known deterministic findings can be resolved through policy rules. Ambiguous or review-relevant findings can receive AI assistance while remaining subject to explicit escalation and human review.



\## Current Limitations



The v1.0 architecture intentionally does not implement:



\- production-grade SCA/license detection

\- persistent enterprise approval workflows

\- authentication or role-based authorization

\- cloud deployment

\- complete persistence of retrieved RAG evidence inside each decision record

\- statistically calibrated LLM confidence scores



These are system boundaries rather than claims of functionality.

