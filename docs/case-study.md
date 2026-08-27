\# Case Study: Building an Auditable AI-Assisted OSS Compliance Workflow



\## Problem



Open source compliance is a useful example of an enterprise workflow in which deterministic automation and AI reasoning have different responsibilities.



Many tasks should be deterministic and reproducible:



\- repository scanning

\- license identification where evidence is available

\- risk classification

\- SPDX generation

\- organization-specific policy evaluation



Other situations contain uncertainty and may benefit from contextual assistance:



\- unknown or ambiguous license findings

\- interpretation of compliance implications

\- remediation recommendations

\- escalation decisions



The goal of this project was therefore not to let an LLM make compliance decisions autonomously.



The goal was to design an architecture in which AI can assist a deterministic enterprise workflow while remaining bounded, traceable, and subject to human review.



\## Architecture



The system evolved into several distinct layers:



```text

User Request

&#x20;    |

Request Planner

&#x20;    |

Workflow Executor

&#x20;    |

&#x20;    +---- Repository Scanner

&#x20;    |

&#x20;    +---- SPDX Generation

&#x20;    |

&#x20;    +---- Risk Classification

&#x20;    |

&#x20;    +---- Policy-as-Code

&#x20;    |

&#x20;    +---- RAG / Knowledge Retrieval

&#x20;    |

&#x20;    +---- Structured AI Advice

&#x20;    |

&#x20;    +---- Governance Decision Record

&#x20;    |

Human Review / Final Decision

```



Workflow execution is correlated through a unique run ID and recorded through an audit trail.



A more detailed architecture description is available in \[architecture.md](architecture.md).



\## Deterministic Logic



Deterministic logic is used wherever the system has sufficient structured evidence and explicit rules.



Examples include:



\- scanning repository files

\- normalizing findings

\- generating SPDX information

\- mapping findings to risk categories

\- applying predefined policy decisions

\- validating workflow dependencies



This is important because these operations should be reproducible.



Running the same policy against the same deterministic evidence should not depend on LLM sampling behavior.



\## Where AI Is Used



AI is used as an advisory layer rather than as the authoritative policy engine.



The AI receives structured scan results and produces structured compliance advice containing:



\- executive summary

\- detected licenses

\- risk assessment

\- recommended compliance actions

\- legal-review recommendation

\- disclaimer



Structured output makes the AI response easier to validate and integrate into downstream workflow logic than unrestricted free-form text.



The AI recommendation remains distinct from the final governance decision.



\## Why RAG Is Used



The project uses Retrieval-Augmented Generation to provide the AI layer with relevant compliance and license knowledge.



Instead of relying exclusively on the model's internal knowledge, relevant information can be retrieved from an indexed knowledge base and supplied as context.



This architecture provides a path toward organization-specific knowledge such as:



\- internal OSS policies

\- approved license guidance

\- compliance procedures

\- legal guidance

\- governance documentation



RAG does not guarantee correctness. Retrieval quality depends on the indexed documents, retrieval strategy, and relevance of the returned context.



\## Policy-as-Code



An important architectural decision was to keep policy outside the LLM.



License policy can produce deterministic outcomes such as:



```text

Approved

Review Required

Legal Review Required

Manual Review

Blocked / High Review

```



This makes policy inspectable and testable.



The LLM may explain or recommend actions around a policy result, but it does not silently redefine organizational policy.



\## Governance and Auditability



AI-assisted decisions require more than logging the final model response.



The workflow therefore records execution events and creates Governance Decision Records for review-relevant findings.



A decision record can contain:



\- deterministic finding and evidence

\- workflow run ID

\- AI provider and model

\- AI recommendation

\- uncertainty

\- human-review requirement

\- final decision

\- timestamp



A central design rule is:



```text

AI recommendation != final governance decision

```



For unresolved findings, the final decision remains unset until a human decision is made.



This prevents the existence of an AI recommendation from being represented as an authorized compliance decision.



\## Uncertainty and Human Review



The system does not invent numerical confidence scores for the LLM.



No statistical calibration was implemented that would justify interpreting a value such as `87% confidence` as a measured probability of correctness.



Instead, uncertainty is represented explicitly when deterministic evidence is insufficient.



For example:



```text

License: UNKNOWN

Risk: Unknown Risk

Policy Decision: Manual Review



Uncertainty:

License could not be determined from deterministic scan evidence.



Human Review Required:

True

```



This is less sophisticated than a calibrated probabilistic confidence model, but it is more defensible than presenting unsupported precision.



\## Testing and CI



The project includes automated tests covering components such as:



\- AI output schema

\- audit logging

\- prompts

\- knowledge loading

\- policy engine

\- RAG retrieval

\- security filtering

\- Governance Decision Records



The v1.0 release candidate passes:



```text

24 tests

```



GitHub Actions executes the project test suite automatically.



\## Limitations



This project is a portfolio/reference implementation rather than a production Software Composition Analysis or legal compliance platform.



Important limitations include:



\- license detection is much simpler than mature SCA tooling

\- LLM recommendations remain probabilistic

\- AI output may contain incorrect interpretations

\- RAG does not guarantee factual correctness

\- retrieved evidence is not fully persisted in every Governance Decision Record

\- AI advice is currently produced at workflow level rather than independently for every finding

\- human approval is represented architecturally but not implemented as a persistent enterprise approval system

\- authentication and role-based authorization are outside the project scope

\- no production cloud deployment is included

\- the system does not provide legal advice



These limitations are explicit system boundaries rather than hidden assumptions.



\## Lessons Learned



\### 1. Not every enterprise problem needs AI



Several important compliance decisions are better implemented using deterministic code and explicit policy.



AI becomes useful where interpretation, explanation, contextual knowledge, or ambiguity enters the workflow.



\### 2. AI architecture is more than an API call



The important engineering work is around the model:



```text

planning

retrieval

structured input

structured output

policy

execution control

auditability

uncertainty

human oversight

```



\### 3. Policy should not disappear into prompts



Moving policy into deterministic configuration makes behavior easier to inspect, test, and govern.



\### 4. RAG improves grounding but does not eliminate uncertainty



Retrieval provides context. It does not mathematically guarantee that the retrieved information is sufficient or that the model will interpret it correctly.



\### 5. Auditability must be designed into the workflow



Adding logs after an AI system has been built is not equivalent to designing traceability into execution.



Run IDs, structured events, deterministic evidence, and decision records need to be part of the architecture.



\### 6. Human oversight needs a technical boundary



Simply stating that "a human is responsible" is insufficient.



The data model should distinguish between:



```text

AI recommendation

```



and:



```text

Final decision

```



That distinction became one of the central architectural principles of the project.



\## Result



The final project is not intended to compete with mature OSS scanning products.



Its purpose is to demonstrate a broader Enterprise AI engineering pattern:



> Combine deterministic systems, organizational policy, retrieval, probabilistic AI reasoning, auditability, and human governance without allowing the LLM to become the uncontrolled decision authority.



That architectural pattern is applicable beyond OSS compliance to other governed enterprise AI workflows.

