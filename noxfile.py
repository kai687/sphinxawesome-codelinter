"""Nox sessions."""

import nox
from nox_poetry import Session, session

nox.options.sessions = ["tests", "lint", "mypy", "safety"]
locations = ["src", "tests", "noxfile.py"]
python_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    deps = ["coverage[toml]", "pytest", "pytest-cov", "yamllint"]
    session.install(".", *deps)
    session.run("pytest", *args)


@session(python=python_versions)
def lint(session: Session) -> None:
    """Lint with ruff."""
    if "--fix" in session.posargs:
        args = ["--fix", *locations]
    else:
        args = session.posargs or locations

    deps = [
        "ruff",
    ]
    session.install(".", *deps)
    session.run("ruff", *args)


@session(python=python_versions[-1])
def black(session: Session) -> None:
    """Format code with Black."""
    args = session.posargs or locations
    session.install(".", "black")
    session.run("black", *args)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Check types with Mypy."""
    args = session.posargs or ["--strict", "--no-warn-unused-ignores"]
    deps = [
        "mypy",
        "types-docutils",
        "nox",
        "pytest",
        "sphinx",
        "nox-poetry",
    ]
    session.install(".", *deps)
    session.run("mypy", *args)


@session(python=python_versions[-1])
def safety(session: Session) -> None:
    """Check for insecure dependencies with safety."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", f"--file={requirements}", "--full-report")


@session(python=python_versions[-1])
def coverage(session: Session) -> None:
    """Upload coverage report."""
    session.install(".", "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
