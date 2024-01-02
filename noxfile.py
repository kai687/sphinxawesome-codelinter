"""Nox sessions."""
from __future__ import annotations

import tempfile

import nox

nox.options.stop_on_first_error = True
nox.options.sessions = ["tests", "lint", "mypy", "safety"]
locations = ["src", "tests", "noxfile.py"]
python_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]
session_install = nox.Session.install


class PoetryNoxSession(nox.Session):
    """Class for monkey-patching the Session object."""

    def export(self: PoetryNoxSession, group: str, file_name: str) -> None:
        """Export a group's dependencies from poetry.

        Args:
            group: The name of a dependency group from the pyproject.toml file
            file_name: The file name for exporting the dependencies.
        """
        self.run(
            "poetry",
            "export",
            "--without-hashes",
            "--with",
            group,
            "--output",
            file_name,
            external=True,
        )

    def install(self: PoetryNoxSession, group: str, *args: str) -> None:
        """Install a group's dependencies into the nox virtual environment.

        To make Nox use the version constraints as defined in pyproject.toml,
        export the dependencies into a temporary file requirements.txt.

        Args:
            group: The dependency group to export
            *args: The packages to install, passed on to the nox.Session.install method.
        """
        with tempfile.NamedTemporaryFile() as requirements:
            self.export(group, requirements.name)
            session_install(self, "-r", requirements.name, *args)


# Monkey-patch nox
nox.Session.install = PoetryNoxSession.install
nox.Session.export = PoetryNoxSession.export


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    deps = ["coverage[toml]", "pytest", "pytest-cov", "sphinx", "yamllint"]
    session.install("dev", ".", *deps)
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session: nox.Session) -> None:
    """Lint with ruff."""
    deps = ["ruff"]
    session.install("lint", ".", *deps)
    session.run("ruff", ".")


@nox.session(python=python_versions[-1])
def fmt(session: nox.Session) -> None:
    """Format code."""
    deps = ["ruff", "black"]
    session.install("lint", ".", *deps)
    session.run("ruff", "check", ".", "--select", "I", "--fix")
    session.run("black", ".")


@nox.session(python=["3.8", "3.12"])
def mypy(session: nox.Session) -> None:
    """Check types with Mypy."""
    args = session.posargs or ["--strict"]
    deps = [
        "mypy",
        "types-docutils",
        "nox",
        "pytest",
        "sphinx",
    ]
    session.install("dev", *deps)
    session.run("mypy", *args)


@nox.session(python=python_versions[-1])
def safety(session: nox.Session) -> None:
    """Check for insecure dependencies with safety."""
    session.export("dev", "requirements.txt")
    session.install("dev", "safety")
    session.run("safety", "check", "--file=requirements.txt", "--full-report")


@nox.session(python=python_versions[-1])
def coverage(session: nox.Session) -> None:
    """Upload coverage report."""
    session.install("dev", ".", "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
