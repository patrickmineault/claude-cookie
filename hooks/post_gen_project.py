#!/usr/bin/env python
"""Post-generation hook for claude-cookie.

Runs after cookiecutter generates the project structure.
"""

import subprocess
import sys


def main():
    """Initialize git repository and print next steps."""
    print("\n" + "=" * 50)
    print("Project created successfully!")
    print("=" * 50)

    # Try to initialize git
    try:
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from claude-cookie template"],
            check=True,
            capture_output=True,
        )
        print("\nGit repository initialized with initial commit.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\nNote: Could not initialize git repository automatically.")
        print("Run 'git init' manually if needed.")

    print("\nNext steps:")
    print("  1. cd {{ cookiecutter.repo_name }}")
    print("  2. uv venv && source .venv/bin/activate")
    print("  3. uv pip install -e '.[dev]'")
    print("  4. pre-commit install")
    print("\nSee CLAUDE.md for development guidelines.")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
