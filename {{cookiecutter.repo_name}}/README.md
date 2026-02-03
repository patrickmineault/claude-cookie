# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Project Structure

```
{{ cookiecutter.repo_name }}/
├── data/
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned, transformed data
│   └── generated/     # AI-generated or synthetic data
├── docs/              # Documentation
├── notebooks/         # Marimo notebooks for visualization
├── src/{{ cookiecutter.repo_name }}/  # Python package
├── tests/             # Test suite
├── Snakefile          # Pipeline orchestration
└── CLAUDE.md          # AI assistant guidance
```

## Usage

```bash
# Run the data pipeline
snakemake --cores 1

# Run tests
pytest

# Start a marimo notebook
marimo edit notebooks/analysis.py

# Check code quality
ruff check .
ruff format .
```

## Development

See `CLAUDE.md` for detailed development guidelines, including:
- Workflow best practices
- Marimo notebook conventions
- Data processing patterns
