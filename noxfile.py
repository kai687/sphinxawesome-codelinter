"""Run automated tasks."""

from __future__ import annotations

import nox
import nox_uv

nox.options.stop_on_first_error = True
nox.options.sessions = ["tests", "lint", "typecheck"]
nox.options.default_venv_backend = "uv"

project = nox.project.load_toml("pyproject.toml")
supported_python_versions = nox.project.python_versions(project)
python_versions = [supported_python_versions[0], supported_python_versions[-1]]


@nox_uv.session(python=python_versions, uv_groups=["dev"])
def tests(s: nox.Session) -> None:
    """Run unit tests."""
    args = s.posargs or ["--cov"]
    s.run("pytest", *args)


@nox_uv.session(python=python_versions, uv_groups=["dev"])
def lint(s: nox.Session) -> None:
    """Lint with ruff."""
    s.run("ruff", "check", ".")


@nox.session
def fmt(s: nox.Session) -> None:
    """Format code."""
    s.install("ruff")
    s.run("ruff", "check", ".", "--fix")
    s.run("ruff", "format", ".")


@nox_uv.session(python=python_versions, uv_groups=["dev"])
def typecheck(s: nox.Session) -> None:
    """Check type annotations."""
    s.run("pyright")


@nox_uv.session(python=python_versions[-1], uv_groups=["dev"])
def coverage(s: nox.Session) -> None:
    """Upload coverage report."""
    s.run("coverage", "xml", "--fail-under=0")
    s.run("codecov", *s.posargs)
