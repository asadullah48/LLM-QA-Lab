# Clone the repository
git clone https://github.com/YOUR_USERNAME/LLM-QA-Lab.git
cd LLM-QA-Lab

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
uv sync

# Run your first test
python run_qa_suite.py