"""Run automated tasks."""

from __future__ import annotations

import nox

nox.options.stop_on_first_error = True
nox.options.sessions = ["tests", "lint", "typecheck"]
nox.options.default_venv_backend = "uv"

python_versions = ["3.9", "3.13"]


def get_requirements(groups: list[str] | str | None = None) -> list[str]:
    """Load requirements from a `pyproject.toml` file."""
    pyproject = nox.project.load_toml("pyproject.toml")
    pkgs = pyproject["project"]["dependencies"]

    if groups and "dependency-groups" in pyproject:
        for g in groups if isinstance(groups, list) else [groups]:
            pkgs += pyproject["dependency-groups"].get(g, [])

    return pkgs


def install_requirements(
    session: nox.Session, groups: list[str] | str | None = None
) -> None:
    """Install requirements into the session's environment."""
    requirements = get_requirements(groups)
    session.install(*requirements)
    session.install("-e", ".")


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    install_requirements(session, "dev")
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session: nox.Session) -> None:
    """Lint with ruff."""
    install_requirements(session, "dev")
    session.run("ruff", "check", ".")


@nox.session(python=python_versions[-1])
def fmt(session: nox.Session) -> None:
    """Format code."""
    install_requirements(session, "dev")
    session.run("ruff", "check", ".", "--fix")
    session.run("ruff", "format", ".")


@nox.session(python=[python_versions[0], python_versions[-1]])
def typecheck(session: nox.Session) -> None:
    """Check type annotations."""
    install_requirements(session, "dev")
    session.run("pyright")


@nox.session(python=python_versions[-1])
def coverage(session: nox.Session) -> None:
    """Upload coverage report."""
    install_requirements(session, "dev")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
