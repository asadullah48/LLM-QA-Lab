# Clone the repository
git clone https://github.com/asadulah48/LLM-QA-Lab.git
cd LLM-QA-Lab

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
uv sync

# Run your first test
python run_qa_suite.py