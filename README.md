# Synthetic Reasoning Forge (SRF)
**Bridging Mathematical Intuition with Formal Verification**

## Overview
The **Synthetic Reasoning Forge** is an experimental pipeline designed to automate the discovery and formalization of mathematical analogies. By leveraging LLM-driven "analogy mining" and the **Lean 4** theorem prover, the system identifies structural isomorphisms between disparate domains—specifically **Control Theory** and **Systems Biology**.

The core objective is to transform fuzzy mathematical intuition into machine-verifiable proofs, ensuring that cross-domain analogies are not just metaphorical, but formally sound.

## System Architecture
The Forge operates in a three-stage verified loop:

1. **Analogy Mining:** An LLM-agent (Claude) identifies isomorphisms across Mathlib namespaces (e.g., *Stability Theory* $\rightarrow$ *Homeostatic Regulation*).
2. **Auto-Formalization:** The engine generates Lean 4 code representing the synthetic conjecture.
3. **Verification Loop:** The conjecture is passed to the Lean 4 compiler via **LeanDojo**. Errors are piped back to the LLM for iterative correction until the code is formally verified.



## Technical Stack
* **Formal Kernel:** Lean 4
* **Orchestration:** Python 3.14 (Isolated via venv)
* **Integration Layer:** LeanDojo / Lean-client-python
* **Agentic Logic:** Claude Code CLI (Anthropic)
* **Version Control:** Git / GitHub

## Current Status
- [x] Environment isolation (Python 3.14 venv)
- [ ] Lean 4 toolchain initialization (elan/lake) **(In Progress)**
- [ ] Cross-domain analogy mining logic 
- [ ] Automated verification loop integration

## Setup & Installation
```bash
# Clone the repository
git clone [https://github.com/cooperRacheal/synthetic-reasoning-forge.git](https://github.com/cooperRacheal/synthetic-reasoning-forge.git)

# Initialize virtual environment
python3 -m venv venv
source venv/bin/activate

# (Future) Install dependencies
# pip install -r requirements.txt