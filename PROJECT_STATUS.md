# OSS Compliance Assistant

## Project Goal

Build an AI-powered Open Source Software Compliance Assistant that can:

* Scan repositories
* Detect software licenses
* Assess compliance risks
* Export compliance reports
* Answer compliance questions using AI
* Support OSS governance workflows

---

## Current Status

### Completed (Day 1 - 28)

#### Foundations

* Python installed
* VS Code configured
* Git installed
* GitHub repository created
* Virtual environment configured

#### AI & RAG

* OpenAI API integration
* ChromaDB vector database
* License knowledge base
* Semantic search
* Compliance Q&A assistant

#### Repository Scanner

* Repository path scanning
* GitHub repository cloning
* Automatic repository selection
* License file discovery
* License detection

#### Supported Licenses

* MIT
* Apache
* BSD
* MPL
* EPL
* CDDL
* LGPL
* GPL
* AGPL

#### Compliance Features

* Risk classification
* Highest risk calculation
* Repository risk assessment
* SPDX ID mapping

#### Streamlit Dashboard

* Repository scanner UI
* Compliance dashboard
* Risk indicators
* Metrics
* Results table
* Session state handling

#### Export Features

* CSV export
* SPDX JSON export

---

## Current Architecture

GitHub URL
↓
Clone Repository
↓
Find License Files
↓
Detect Licenses
↓
Map SPDX IDs
↓
Calculate Risk
↓
Display Dashboard
↓
Export CSV / SPDX

---

## Next Steps

### Day 29

* Combine Clone + Scan into one workflow
* Improve user experience

### Day 30

* AI Compliance Advisor
* Explain license obligations
* Explain compliance risks

### Day 31

* Enhanced SPDX export
* SPDX metadata
* SPDX relationships

### Day 32+

* Dependency scanning
* SBOM generation
* Policy engine
* Compliance recommendations
* AI governance features

---

## GitHub Repository

license_scanner

## Last Completed Milestone

Day 28:
CSV Export + SPDX Export + Session State
