
# 🛠️ Tools & Technologies – DLM Research Platform

This document tracks all major tools, libraries, and frameworks used in the DLM platform — across quant research, development, operations, and leadership roles.

---

## ⚙️ Core Stack

| Purpose                     | Tool / Language        | Notes |
|-----------------------------|------------------------|-------|
| Programming                 | Python                 | Core language for ingestion, analytics, modeling |
| Database                    | PostgreSQL             | Structured time series + fundamentals DB |
| Frontend (planned)          | React                  | Dashboard + structured trade entry UI |
| Automation                  | Cron                   | Daily scripts for updates, screening, ingestion |
| Data Fetch / APIs           | yfinance, FRED, BEA, SEC Edgar, CFTC CoT, LME, COMEX, IBKR | Full macro + market + positioning + futures data |

---

## 📊 Visualization & Diagramming

| Purpose                        | Tool         | Notes |
|--------------------------------|--------------|-------|
| Architecture & system maps     | Mermaid      | Core diagramming format for code, systems, and workflows |
| Roadmaps & timelines           | Mermaid Gantt| Maintained in roadmap.md |
| Data models / ERDs             | Mermaid (basic), evaluating DBML or PlantUML | Will scale if schema complexity increases |
| Graphs & dependencies          | (TBD) Graphviz / D2 | For risk/strategy trees, cross-factor dependencies |
| UI/UX whiteboarding            | (Optional) Whimsical, Excalidraw | If needed for frontend flows or education docs |

---

## 📚 Documentation

| Purpose              | Tool           | Notes |
|----------------------|----------------|-------|
| Docs authoring       | Markdown in VS Code | Markdown-first workflow using Git |
| Docs preview         | Mermaid Plugin | Live rendering of system diagrams |
| Docs site (planned)  | MkDocs         | Public/private documentation portal |
| Internal wiki        | Confluence     | Structured notes, planning docs, process maps |

---

## 🔁 Version Control & CI/CD

| Purpose            | Tool        | Notes |
|--------------------|-------------|-------|
| Code + data versioning | Git + GitHub | All data pipelines, signals, and model logic |
| CI/CD pipeline      | GitHub Actions (planned) | Auto-generate diagrams/docs, run analytics/tests |
| Change tracking     | Mermaid + changelog + Git | Built-in transparency and audit trail |

---

## 📈 Project Management & Planning

| Purpose              | Tool              | Notes |
|----------------------|-------------------|-------|
| Task management      | JIRA, GitHub Issues | GitHub for dev tasks, JIRA for enterprise PM |
| Documentation        | Confluence        | Broader team planning and BA/process artifacts |
| Roadmapping          | Mermaid Gantt     | Markdown-native versioned timelines |
| Product vision       | `VISION.md`, `ROADMAP.md` | Internal strategy artifacts |
| Workstream automation| Git + Mermaid     | Structured workflows, version-controlled maps |

---

## ✅ Quality Assurance

| Purpose               | Tool           | Notes |
|-----------------------|----------------|-------|
| Unit testing          | pytest         | Core Python test framework for all modules |
| Test case design      | Mermaid QA flowcharts | Visualize test coverage, flows, and outcomes |
| Coverage reports      | coverage.py    | Analyze and report code coverage during test runs |
| CI test integration   | GitHub Actions (planned) | Run all tests in CI pipeline and fail builds if broken |

---

## 🧑‍💼 Role-Based Tooling

| Role                          | Tooling Used                                                  |
|-------------------------------|---------------------------------------------------------------|
| Programme Manager             | JIRA, Mermaid Gantt, VISION.md, ROADMAP.md                    |
| Product Manager               | Markdown + Mermaid mindmap, OpenBB Terminal, KPI tracking     |
| Business Analyst (you)      | Confluence, Mermaid flowcharts, Markdown specs                |
| Functional Architect (you)  | Mermaid flowcharts + state diagrams                           |
| Technical Architect (you) | Mermaid class/ER diagrams, GitHub repos, MkDocs               |
| Developer (you)           | PyCharm, VS Code, Python, PostgreSQL, Git                     |
| Quant / Trader (you)      | IBKR TWS, custom trade models, option structuring tools       |
| Head of Trading (you)     | Weekly wrap-up, changelogs, portfolio dashboards              |
| COO (you)                 | Risk engine, audit logs, data automation, changelog reporting |
| CIO / CTO (you)           | Platform architecture, tech stack design, scaling strategy    |
| CEO / Founder (you)       | Product vision, roadmap ownership, trade review               |
| QA Engineer (you)         | pytest, coverage tracking, QA planning flows                  |

---

## 🔮 Tooling Wishlist / Under Evaluation

| Area                     | Candidate Tools | Notes |
|--------------------------|-----------------|-------|
| BPMN / workflows         | Camunda, draw.io | For enterprise process modeling or change approval |
| Deeper ERDs              | DBML, PlantUML ER| For constraint-rich or normalized schemas |
| Auto-diagram generation  | YAML → Mermaid  | For backtesting roadmap, schema drift, and pipeline trees |
| Testing & coverage       | pytest + Mermaid QA flow | Formalize test case tracking and pipeline testing |
