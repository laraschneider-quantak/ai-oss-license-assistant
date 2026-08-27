\# AI-Assisted OSS Compliance Workflow



A portfolio project demonstrating how deterministic software compliance analysis, policy-as-code, Retrieval-Augmented Generation (RAG), and Large Language Models can be combined in an auditable enterprise AI workflow.



The system scans software repositories for license-related findings, applies deterministic risk and policy logic, generates SPDX output, and uses AI assistance for compliance analysis where additional interpretation is useful.



A central design principle is that \*\*AI recommendations are not treated as final governance decisions\*\*.



\## Why This Project Exists



Open source compliance involves tasks with very different levels of uncertainty.



Some decisions can be handled deterministically:



\- identifying known license information

\- mapping licenses to SPDX identifiers

\- applying predefined risk classifications

\- evaluating organization-specific policy rules



Other situations require additional context or interpretation:



\- unknown or ambiguous licensing

\- explaining compliance implications

\- recommending remediation actions

\- determining when human review should be required



This project explores an enterprise architecture in which deterministic controls remain authoritative while AI provides bounded assistance around those controls.



\## Key Capabilities



\- repository scanning for license-related findings

\- SPDX report generation

\- deterministic license risk classification

\- policy-as-code for compliance decisions

\- typed workflow planning and execution

\- dependency validation between workflow steps

\- structured AI compliance recommendations

\- Retrieval-Augmented Generation (RAG)

\- policy and knowledge retrieval

\- explicit uncertainty and escalation handling

\- human-review indicators

\- workflow audit logging with run IDs

\- AI Governance Decision Records

\- automated tests and GitHub Actions CI

\- Streamlit-based user interface



\## Architecture



The project separates deterministic processing from AI-assisted reasoning.



```text

&#x20;                   User / Repository

&#x20;                          |

&#x20;                          v

&#x20;                   Request Planner

&#x20;                          |

&#x20;                          v

&#x20;                   Workflow Executor

&#x20;                          |

&#x20;             +------------+-------------+

&#x20;             |                          |

&#x20;             v                          v

&#x20;     Deterministic Layer           AI Assistance

&#x20;             |                          |

&#x20;     Repository Scan                RAG Retrieval

&#x20;     SPDX Generation                    |

&#x20;     Risk Classification                v

&#x20;     Policy-as-Code                Policy / Context

&#x20;             |                          |

&#x20;             +------------+-------------+

&#x20;                          |

&#x20;                          v

&#x20;                Structured AI Advice

&#x20;                          |

&#x20;                          v

&#x20;             Governance Decision Record

&#x20;                          |

&#x20;                   Human Review

&#x20;                          |

&#x20;                          v

&#x20;                    Final Decision

```



\### Deterministic Layer



The deterministic layer performs operations that should not depend on probabilistic model behavior.



Examples include:



\- repository scanning

\- SPDX mapping

\- risk classification

\- policy decisions

\- workflow dependency validation



This provides a reproducible baseline for compliance analysis.



\### AI-Assisted Layer



AI is used to provide structured compliance guidance based on scan findings and retrieved context.



AI output is represented through a structured schema containing information such as:



\- executive summary

\- detected licenses

\- risk assessment

\- compliance actions

\- legal-review recommendation

\- disclaimer



The AI recommendation does not automatically become the final compliance decision.



\## Retrieval-Augmented Generation



The project includes a RAG pipeline using OpenAI embeddings and ChromaDB.



Compliance and policy knowledge can be indexed and retrieved semantically. Retrieved information is then supplied as context to the AI layer.



This reduces reliance on the model's parametric knowledge and allows responses to be grounded in project-specific compliance knowledge.



RAG retrieval activity is also included in the audit trail.



\## Policy-as-Code



License policy decisions are separated from the AI model.



The policy layer can classify licenses into outcomes such as:



```text

Approved

Review Required

Legal Review Required

Manual Review

Blocked / High Review

```



This separation is intentional.



Organizational policy should remain deterministic and inspectable rather than being implicitly encoded inside an LLM prompt.



\## AI Governance Decision Records



For findings requiring review, the workflow can create an auditable governance record containing:



\- decision ID

\- workflow run ID

\- finding

\- deterministic evidence

\- retrieved context reference where available

\- AI provider and model

\- AI recommendation

\- uncertainty

\- human-review requirement

\- final decision

\- UTC timestamp



Example:



```text

Finding:

external\_repos/example/LICENSE



Deterministic Evidence:

License: UNKNOWN

Risk: Unknown Risk

Policy Decision: Manual Review



AI Recommendation:

Manual investigation is required before distribution.



Uncertainty:

License could not be determined from deterministic scan evidence.



Human Review Required:

True



Final Decision:

None

```



`Final Decision: None` is intentional until an authorized human decision is recorded.



This explicitly separates:



```text

AI recommendation != final governance decision

```



\## Auditability



Workflow execution produces audit events containing information such as:



\- run ID

\- repository

\- workflow step

\- execution status

\- AI/RAG activity



The shared run ID allows events belonging to the same workflow execution to be correlated.



The goal is not to build a full governance platform, but to demonstrate the architectural controls required for traceable AI-assisted enterprise workflows.



\## Example Workflow



A typical request follows this sequence:



```text

Repository

&#x20;   |

&#x20;   v

Scan repository

&#x20;   |

&#x20;   +--> Known license --> deterministic policy decision

&#x20;   |

&#x20;   +--> Unknown / review finding

&#x20;                        |

&#x20;                        v

&#x20;                   AI assistance

&#x20;                        |

&#x20;                        v

&#x20;               Governance record

&#x20;                        |

&#x20;                        v

&#x20;                   Human review

```



Example scan result:



```text

Apache-2.0

Risk: Low Risk

Policy Decision: Approved



UNKNOWN

Risk: Unknown Risk

Policy Decision: Manual Review

```



The known finding can be handled through deterministic rules. The unknown finding is explicitly escalated rather than silently classified by the AI model.



\## Running the Project



\### Requirements



\- Python 3.14

\- OpenAI API key



Install dependencies:



```bash

pip install -r requirements.txt

```



Create a local `.env` file:



```text

OPENAI\_API\_KEY=your\_api\_key

```



`.env` is excluded from version control.



\### Run the Compliance Workflow



```bash

python compliance\_workflow.py

```



\### Run the Agent



```bash

python agent.py

```



\### Run the Streamlit Application



```bash

streamlit run app.py

```



\### Build the RAG Index



```bash

python build\_chroma\_index.py

```



\## Testing



Run the project test suite with:



```bash

python -m pytest -q

```



Current v1.0 release candidate:



```text

24 passed

```



Test discovery is scoped to the project's `tests/` directory so that tests contained in externally scanned repositories are not executed as part of this project's test suite.



\## Continuous Integration



GitHub Actions executes the Python test suite on repository changes.



The CI workflow:



1\. checks out the repository

2\. configures Python

3\. installs dependencies

4\. executes the project tests



This provides automated regression validation for the portfolio release.



\## Security and Repository Hygiene



Local and potentially sensitive runtime artifacts are excluded from version control, including:



```text

.env

venv/

chroma\_db/

external\_repos/

\*.log

```



External repositories are treated as scan targets rather than project source code.



\## Limitations



This is a portfolio and reference implementation, not a production compliance platform.



Known limitations include:



\- license detection is intentionally limited compared with mature commercial or open-source SCA platforms

\- AI recommendations are probabilistic and may be incorrect

\- AI output is not legal advice

\- human review remains necessary for ambiguous or high-risk findings

\- RAG quality depends on the indexed knowledge base

\- retrieved RAG context is not currently persisted in every individual Governance Decision Record

\- AI recommendations are currently generated at workflow level rather than independently for every finding

\- the project does not implement enterprise authentication or authorization

\- no production cloud deployment is provided

\- the dependency file reflects the tested development environment and contains transitive dependencies



These limitations are intentionally documented rather than hidden behind the AI layer.



\## Design Principles



The project follows several principles relevant to enterprise AI engineering:



1\. \*\*Deterministic controls before probabilistic reasoning\*\*

2\. \*\*Policy outside the model\*\*

3\. \*\*Structured AI outputs\*\*

4\. \*\*Explicit uncertainty\*\*

5\. \*\*Human oversight for consequential decisions\*\*

6\. \*\*Traceability through audit records\*\*

7\. \*\*AI recommendations are not final decisions\*\*



\## Technology Stack



\- Python

\- OpenAI API

\- LangChain

\- ChromaDB

\- Pydantic

\- Streamlit

\- Git / GitHub

\- GitHub Actions

\- pytest

\- SPDX



\## Project Status



\*\*v1.0 Portfolio Release candidate\*\*



The project is feature-frozen for v1.0.



Remaining release work is focused on documentation, examples, repository cleanup, and release packaging rather than additional functionality.



\## Future Work



Potential future improvements could include:



\- stronger license detection using dedicated SCA tooling

\- persistent human decision workflows

\- richer evidence provenance for retrieved RAG context

\- enterprise identity and authorization

\- policy versioning

\- production observability

\- deployment architecture



These are intentionally outside the scope of v1.0.

