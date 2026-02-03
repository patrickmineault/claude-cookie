# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Folder Structure

```
{{ cookiecutter.repo_name }}/
├── data/
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned, transformed data
│   └── generated/     # AI-generated or synthetic data
├── docs/              # Documentation
├── notebooks/         # Marimo notebooks for visualization
├── src/
│   └── {{ cookiecutter.repo_name }}/  # Python package for data processing
├── tests/             # Test suite
├── Snakefile          # Pipeline orchestration
└── pyproject.toml     # Project configuration
```

**Data lineage rules:**
- `data/raw/` is immutable - never modify files here
- `data/processed/` contains outputs from `src/` processing code
- `data/generated/` contains AI-generated data (mark clearly)
- Notebooks read from `data/processed/`, never write to `data/raw/`

## Package Management

This project uses `uv` for fast, reliable Python package management.

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # Unix/macOS
# .venv\Scripts\activate   # Windows

# Install project with dev dependencies
uv pip install -e ".[dev]"

# Add a new dependency
uv pip install <package>
```

## Workflow Guidelines

### Plan-Execute-Evaluate Loop

Use **Shift+Tab** to enter plan mode before executing. Iterate on the plan before running code. This prevents:
- Unproductive rabbit holes
- Wasted tokens on bad approaches
- Accumulating cruft and complexity

Use **Esc** liberally to stop and redirect when things go off track.

### Separation of Concerns

- **`src/` package**: Pure Python for data processing. No visualization code here.
- **`notebooks/`**: Visualization and exploration with Marimo. Reads processed data.

This separation matters because:
- Processing code changes rarely; visualization iterates constantly
- Processing should be reproducible; notebooks are exploratory
- Tests cover processing logic; visualizations are validated by inspection

### Test-Driven Development

When AI writes code, tests are how you verify it works correctly.

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

Write tests before or alongside new processing code. Tests catch:
- Incorrect data reading
- Wrong transformations
- Subtle bugs that bypass visual inspection

## Marimo

The notebooks in `notebooks/` use Marimo.  Marimo notebooks are reactive computational notebooks written in standard Python with annotations. Unlike traditional notebooks, cells form a directed acyclic graph (DAG) and automatically re-execute when their dependencies change.

### Critical Rules

1. **No variable redeclaration** — Each variable can only be defined in one cell
2. **No circular dependencies** — The dependency graph must be acyclic
3. **UI values require separate cells** — Access `.value` in a different cell than where the UI element is defined
4. **Underscore prefix = cell-local** — Variables like `_temp` won't be visible to other cells

### Cell Structure

Only edit code inside `@app.cell`. Marimo handles function parameters and returns:

```python
@app.cell
def _():
    # your code here
    return
```

### Quick Reference

- **Display**: Last expression auto-displays (like Jupyter)
- **Markdown**: `mo.md("# Title")`
- **Layout**: `mo.hstack([a, b])`, `mo.vstack([a, b])`, `mo.tabs({"Tab1": content})`
- **SQL**: `df = mo.sql(f"""SELECT * FROM table""")`
- **Plots**: Return figure directly; for matplotlib use `plt.gca()` not `plt.show()`
- **Data**: Prefer polars over pandas

### Example: Reactive UI

```python
@app.cell
def _():
    import marimo as mo
    import altair as alt
    import polars as pl
    return

@app.cell
def _():
    n_points = mo.ui.slider(10, 100, value=50, label="Number of points")
    n_points  # display the slider
    return

@app.cell
def _():
    # This cell re-runs automatically when slider changes
    df = pl.DataFrame({
        "x": np.random.rand(n_points.value),
        "y": np.random.rand(n_points.value)
    })
    alt.Chart(df).mark_circle().encode(x="x", y="y")
    return
```

### Common Mistakes

| Problem | Solution |
|---------|----------|
| "Variable already defined" | Move definition to a single cell, reference elsewhere |
| "Cycle detected" | Reorganize so cell A doesn't depend on B while B depends on A |
| UI value is stale/None | Access `.value` in a downstream cell, not where UI is created |

### After Editing

Run `marimo check --fix` to catch formatting issues and common pitfalls.

## Visualization Philosophy

Generate **many cheap diagnostic plots** to validate your data. Individually low-utility plots collectively help convince you the data is correct.

Don't trust processing code blindly - visualize intermediate outputs. Turn hunches from plots into formal tests as analysis matures.

## Context Management

Keep Claude Code's context clean for better results:

- `/clear` - Start fresh when switching tasks
- `/compact` - Compress context when it gets long
- Write handoff notes in this file when stopping work mid-task
- Document solutions to difficult bugs here so they don't get reintroduced

## Code Quality

This project uses **ruff** for linting and formatting, enforced via pre-commit hooks.

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Or run ruff directly
ruff check .
ruff format .
```

**Maintenance practices:**
- Be aggressive about culling dead code (git means you don't lose anything)
- Name things well, rename when function changes
- Ask Claude to identify dead code and refactor
- Write tests before refactoring so you know it worked

## Git Workflow

Use branches for experiments. Delete code with impunity knowing you have infinite backups.

```bash
# Create a branch for experiments
git checkout -b experiment/new-feature

# If it works, merge
git checkout main
git merge experiment/new-feature

# If it fails, just delete
git branch -D experiment/new-feature
```

## Pipeline

The `Snakefile` defines the data processing pipeline as a DAG:

```
data/raw/ → src/ processing → data/processed/ → notebooks/
```

```bash
# Dry run to see what would execute
snakemake --dry-run

# Run the pipeline
snakemake --cores 1

# Force re-run a specific rule
snakemake --forcerun <rule_name>
```

Benefits:
- Tracks which outputs are stale
- Reproduces results with one command
- Documents the computational graph
