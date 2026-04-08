# Project Constitution (claude.md)

## Project: Scaper
## Protocol: B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger)
## Architecture: A.N.T. 3-Layer

---

## Architectural Invariants

1. **No code in `tools/` until Discovery is complete and Data Schema is approved.**
2. **`gemini.md` is the single source of truth for schemas and rules.**
3. **All temporary/intermediate files go in `.tmp/`.**
4. **If logic changes, update the SOP in `architecture/` before updating code.**
5. **Self-Annealing:** Every error leads to a fix, a test, and an architecture update.

---

## Data Schemas
_Defined in `gemini.md`. Pending Discovery._

## Behavioral Rules
_Pending Discovery._

## Directory Map

```
.
├── claude.md          # Project Constitution (this file)
├── gemini.md          # Data Schemas & Maintenance Log
├── task_plan.md       # Phases, goals, checklists
├── findings.md        # Research, discoveries, constraints
├── progress.md        # Action log, errors, test results
├── .env               # API Keys/Secrets (verified in Link phase)
├── architecture/      # Layer 1: SOPs (Markdown)
├── tools/             # Layer 3: Python Scripts (Deterministic)
└── .tmp/              # Temporary Workbench (Ephemeral)
```

## Status
- **Current Phase:** 1 - Blueprint (Discovery)
- **Blocking:** Awaiting user answers to Discovery Questions
