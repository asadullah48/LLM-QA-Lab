[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Tests](https://img.shields.io/badge/tests-100%25-brightgreen)]()
[![Ollama](https://img.shields.io/badge/ollama-supported-blue)]()
# Clone the repository
git clone https://github.com/asadulah48/LLM-QA-Lab.git
cd LLM-QA-Lab

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
uv sync

# Run your first test
python run_qa_suite.py
