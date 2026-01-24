"""Run automated tasks."""

from __future__ import annotations

import nox

nox.options.stop_on_first_error = True
nox.options.sessions = ["tests", "lint", "typecheck"]
nox.options.default_venv_backend = "uv"

project = nox.project.load_toml("pyproject.toml")
supported_python_versions = nox.project.python_versions(project)
python_versions = [supported_python_versions[0], supported_python_versions[-1]]


dev_dependencies = nox.project.dependency_groups(project, "dev")


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    session.install("-e", ".")
    session.install(*dev_dependencies)
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session: nox.Session) -> None:
    """Lint with ruff."""
    session.install(*dev_dependencies)
    session.run("ruff", "check", ".")


@nox.session(python=python_versions[-1])
def fmt(session: nox.Session) -> None:
    """Format code."""
    session.install("ruff")
    session.run("ruff", "check", ".", "--fix")
    session.run("ruff", "format", ".")


@nox.session(python=python_versions)
def typecheck(session: nox.Session) -> None:
    """Check type annotations."""
    session.install(*dev_dependencies)
    session.run("pyright")


@nox.session(python=python_versions[-1])
def coverage(session: nox.Session) -> None:
    """Upload coverage report."""
    session.install(*dev_dependencies)
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
