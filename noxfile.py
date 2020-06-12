"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

nox.options.sessions = ["tests", "lint", "mypy", "pytype", "safety"]
locations = ["src", "tests", "noxfile.py"]


def install_constrained_version(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages with version constraints from poetry.lock."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            "--dev",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.6", "3.7", "3.8"])
@nox.parametrize("sphinx", ["2.*", "3.*"])
def tests(session: Session, sphinx: str) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_constrained_version(session, "coverage[toml]", "pytest", "pytest-cov")
    # override the default Sphinx version (which will be 3.x)
    session.run("poetry", "run", "pip", "install", f"sphinx=={sphinx}", external=True)
    session.run("pytest", *args)
    session.run(
        "poetry",
        "run",
        "python3",
        "-c",
        "import sphinx; print(sphinx.__version__)",
        external=True,
    )


@nox.session(python=["3.6", "3.7", "3.8"])
def lint(session: Session) -> None:
    """Lint with Flake8."""
    args = session.posargs or locations
    install_constrained_version(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Format code with Black."""
    args = session.posargs or locations
    install_constrained_version(session, "black")
    session.run("black", *args)


@nox.session(python=["3.6", "3.7", "3.8"])
def mypy(session: Session) -> None:
    """Check types with Mypy."""
    args = session.posargs or locations
    install_constrained_version(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.6", "3.7", "3.8"])
def pytype(session: Session) -> None:
    """Check types with Pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_constrained_version(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=["3.6", "3.7", "3.8"])
def typeguard(session: Session) -> None:
    """Check types at runtime with typeguard."""
    # can I get this from importlib.meta too?
    package = "sphinxawesome.codelinter"
    session.run("poetry", "install", "--no-dev", external=True)
    install_constrained_version(session, "pytest", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Check for insecure dependencies with safety."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        install_constrained_version(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage report."""
    install_constrained_version(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
