# LLM QA Lab

![Agentic AI](https://img.shields.io/badge/Agentic-AI-blue)
![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![Ollama](https://img.shields.io/badge/ollama-supported-blue)

A quality-assurance harness for LLM outputs: run a set of test cases
against a model, score the responses, and get a pass/fail report. Built
around a local Ollama model by default — no API key or cloud dependency
required to try it.

## Status

This corrects a previous README that was unformatted (raw shell commands
with no code fence), had a typo'd clone URL, and carried an MIT-license
badge with no `LICENSE` file in the repo. Fixed the clone URL and dropped
the license badge below until a `LICENSE` file exists.

The bundled `config/default.yaml` declares six test suites (`accuracy`,
`robustness`, `safety`, `bias`, `rag`, `consistency`) — **only `accuracy`
is implemented today** (`src/tests/test_accuracy.py`). The other five are
config placeholders, not working code; see Roadmap.

## What it does

- `run_qa_suite.py` runs the accuracy suite's 3 built-in test cases
  against the configured model, scores each response (exact-match and
  partial word-overlap scoring), and prints a Rich-formatted results
  table.
- `compare_models.py` runs the same question set against two named Ollama
  models side by side.
- `LLMClient` (`src/core/llm_client.py`) calls a local Ollama server over
  plain `urllib` (no SDK dependency) and **falls back to a mock
  responder automatically if Ollama isn't reachable** — verified by
  running the suite with no Ollama process running; it printed a clear
  warning and completed with mock responses rather than crashing.

## Getting started

```bash
git clone https://github.com/asadullah48/LLM-QA-Lab.git
cd LLM-QA-Lab

uv venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
uv sync

python run_qa_suite.py          # works with or without Ollama running
```

For real (non-mock) responses, install [Ollama](https://ollama.com), pull
a model (`ollama pull gemma3:4b` — the config default), and run
`ollama serve` before the suite.

## Project structure

```
config/
  default.yaml           Provider config + the 6 declared test suites
src/
  core/llm_client.py      Ollama client with mock fallback
  tests/test_accuracy.py  The one implemented test suite
  utils/                  Config loader, logging
run_qa_suite.py            CLI entry point (Rich table output)
compare_models.py          Side-by-side model comparison script
```

## 🧭 Agentic AI Alignment

- **Autonomy** — none yet: this is an evaluation *harness*, not an agent.
  It runs a fixed test set and scores the output; it doesn't decide what
  to test next based on results.
- **Resilience** — real and verified: `LLMClient` degrades to a mock
  responder rather than failing the whole suite when the configured
  provider is unreachable, which is exactly the kind of failure-handling
  an agent's own eval loop would need.
- **Adaptivity** — the provider abstraction (`config/default.yaml`'s
  `llm.providers`) already lists ollama/openai/anthropic/groq, but only
  ollama is wired up in `llm_client.py` today; the others are config,
  not code (see Roadmap).

## 📈 Roadmap

- [ ] Implement the five declared-but-missing test suites (robustness,
      safety, bias, rag, consistency) or remove them from
      `config/default.yaml` until they exist
- [ ] Wire up the OpenAI/Anthropic/Groq providers listed in config —
      `llm_client.py` only implements Ollama right now
- [ ] Add a `LICENSE` file (MIT, matching the intent of the original badge)
- [ ] Fill in real author metadata in `pyproject.toml` (currently
      `"Your Name" <your.email@example.com>`)
- [ ] CI running `run_qa_suite.py` in mock mode on push

## 👨‍💻 Author

Built by **Asadullah Shafique**

🔗 Explore my portfolio showcasing Agentic AI projects and real-world
applications: [asadullahshafique-devunity.vercel.app](https://asadullahshafique-devunity.vercel.app)
