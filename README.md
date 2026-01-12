# Synthetic Reasoning Forge (SRF)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Lean 4](https://img.shields.io/badge/Lean-4.26.0-orange.svg)](https://lean-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Bridging Mathematical Intuition with Formal Verification**

## Overview

The **Synthetic Reasoning Forge** is an experimental pipeline designed to automate the discovery and formalization of mathematical analogies. By leveraging LLM-driven "analogy mining" and the **Lean 4** theorem prover, the system identifies structural isomorphisms between disparate domains—specifically **Control Theory** and **Systems Biology**.

The core objective is to transform fuzzy mathematical intuition into machine-verifiable proofs, ensuring that cross-domain analogies are not just metaphorical, but formally sound.

## System Architecture

The Forge operates in a three-stage verified loop:

1. **Analogy Mining:** An LLM-agent (Claude) identifies isomorphisms across Mathlib namespaces (e.g., *Stability Theory* → *Homeostatic Regulation*).
2. **Auto-Formalization:** The engine generates Lean 4 code representing the synthetic conjecture.
3. **Verification Loop:** The conjecture is passed to the Lean 4 compiler via **LeanDojo**. Errors are piped back to the LLM for iterative correction until the code is formally verified.

## Technical Stack

| Component | Technology |
|-----------|------------|
| **Formal Kernel** | Lean 4 (v4.26.0) |
| **Orchestration** | Python 3.11+ (isolated via `.venv`) |
| **Integration Layer** | LeanDojo / lean-client-python |
| **Agentic Logic** | Claude Code CLI (Anthropic) |
| **Build System** | pyproject.toml / hatchling |
| **Version Control** | Git / GitHub |

## Project Structure

```
reasoning_forge/
├── pyproject.toml    # Package manifest & tool config
├── README.md         # This file
├── CLAUDE.md         # AI governance & project memory
├── data/             # Raw math problems & datasets
├── scripts/          # Automation utilities
├── src/logic/        # Python bridge & heuristics
├── tests/            # Pytest suite
└── lean/             # Lean 4 formal verification
    ├── ForgeLogic.lean   # Theorem definitions
    ├── lakefile.toml     # Lake build config
    └── lean-toolchain    # Pinned Lean version
```

## Current Status

- [x] Environment isolation (Python 3.11+ venv)
- [x] Lean 4 toolchain initialization (elan/lake)
- [x] Package manifest (`pyproject.toml`)
- [ ] Cross-domain analogy mining logic
- [ ] Python ↔ Lean communication bridge
- [ ] Automated verification loop integration

## Prerequisites

Before installation, ensure you have:

- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **elan** (Lean version manager) — [Install guide](https://github.com/leanprover/elan)
- **Git** — For version control

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/cooperRacheal/synthetic-reasoning-forge.git
cd synthetic-reasoning-forge

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"

# Build Lean project
cd lean && lake build
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

This project is in early development. Contributions are welcome! Please open an issue to discuss changes before submitting a pull request.
