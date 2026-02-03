# claude-cookie

A cookiecutter template for scientific data analysis projects, designed for AI-assisted development with Claude Code.

Spiritual successor to [true-neutral-cookiecutter](https://github.com/patrickmineault/true-neutral-cookiecutter), updated for modern Python tooling and AI-assisted workflows.

## Quick Start

### New Project

```bash
# Install cookiecutter if needed
pip install cookiecutter

# Create a new project
cookiecutter gh:patrickmineault/claude-cookie
```

### Existing Project

Copy `CLAUDE.md.template` to your project as `CLAUDE.md` and adapt it.

## What's Included

```
your_project/
├── data/
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned, transformed data
│   └── generated/     # AI-generated data
├── docs/              # Documentation
├── notebooks/         # Marimo notebooks
├── src/your_project/  # Python package
├── tests/             # Test suite
├── CLAUDE.md          # AI assistant guidance
├── Snakefile          # Pipeline orchestration
├── pyproject.toml     # Project config (uv, ruff, pytest)
└── .pre-commit-config.yaml  # Code quality hooks
```

## Evolution from true-neutral-cookiecutter

| Original | claude-cookie | Why |
|----------|--------------|-----|
| `data/` | `data/raw/`, `data/processed/`, `data/generated/` | Clear data lineage |
| `scripts/` | `notebooks/` | Marimo-first for visualization |
| `setup.py` | `pyproject.toml` | Modern packaging with uv |
| — | `Snakefile` | Pipeline orchestration |
| — | `CLAUDE.md` | AI workflow guidance |
| — | `.pre-commit-config.yaml` | Automatic code quality |

## Philosophy

This template embodies best practices for AI-assisted scientific coding:

1. **Separate processing from visualization** — `src/` for data processing, `notebooks/` for exploration
2. **Explicit data lineage** — Know where your data comes from and what's been done to it
3. **Test-driven development** — Tests verify AI-generated code works correctly
4. **Pipeline orchestration** — Snakemake tracks dependencies and ensures reproducibility
5. **Context management** — `CLAUDE.md` helps AI assistants understand your project

See the included `CLAUDE.md` for detailed workflow guidelines, including Marimo notebook conventions.

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [cookiecutter](https://cookiecutter.readthedocs.io/)

## License

MIT
