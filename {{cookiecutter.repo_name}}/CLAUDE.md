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
├── scripts/           # Where scripts live. They should leverage scripts including src.
├── src/
│   └── {{ cookiecutter.repo_name }}/  # Python package for data processing
├── tests/             # Test suite
├── Snakefile          # Pipeline orchestration (optional)
└── pyproject.toml     # Project configuration
└── .gitignore
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
uv add <package>
```

Claude should consistently use `uv add` to install new dependencies rather than using pip directly, so that packages
can be tracked.

## Workflow Guidelines

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

**Important note**: While underscores allow local variables in cells without polluting the global namespace, using `_` can make the code less-readable. When cells become long, prefer self-contained over using `_` for every cell.

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

Generate **many cheap diagnostic plots** to validate your data. Individually low-utility plots collectively help convince the user the data is correct.

Don't trust processing code blindly - visualize intermediate outputs. Turn hunches from plots into formal tests as analysis matures.

## Documenting solutions to difficult bugs

Document solutions to difficult bugs in LESSONS_LEARNED.md so they don't get reintroduced.

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
- Name things well, rename when function changes
- Write tests before refactoring

## Pipeline (Optional)

If using Snakemake, the `Snakefile` defines the data processing pipeline as a DAG:

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

Do not force introduction of pipeline unless user asks. If they ask for a specific technology. If you do use pipelining, use it consistently rather than running code directly.
