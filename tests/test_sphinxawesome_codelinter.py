"""Unit tests for the sphinxawesome.codelinter extension."""

import os
from io import StringIO
from pathlib import Path

import pytest
from sphinx.application import Sphinx

from sphinxawesome.codelinter import __version__  # type: ignore


def test_returns_version() -> None:
    """It has the correct version."""
    assert __version__ == "3.0.0b1"


def test_can_access_rootdir(rootdir: Path) -> None:
    """It can access the test files."""
    conf_file = rootdir / "test-root" / "conf.py"
    index_file = rootdir / "test-root" / "index.rst"
    assert conf_file.exists()
    assert index_file.exists()


@pytest.mark.sphinx("dummy")
def test_dummy_compiles_minimal_configuration(app: Sphinx) -> None:
    """It compiles a minimal configuration with the `dummy` builder."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)


@pytest.mark.sphinx(
    "dummy",
    confoverrides={"extensions": ["sphinxawesome.codelinter"]},
)
def test_dummy_compiles_with_extension(app: Sphinx) -> None:
    """It compiles with a minimal configuration with the extension added."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "codelinter_languages" in app.config


@pytest.mark.sphinx(
    "codelinter",
    confoverrides={"extensions": ["sphinxawesome.codelinter"]},
)
def test_codelinter_compiles_without_languages(app: Sphinx, status: StringIO) -> None:
    """It builds with the codelinter builder without any languages."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "codelinter_languages" in app.config
    assert "[Line 6] linting json" not in status.getvalue()
    assert "[Line 10] linting" not in status.getvalue()
    assert "[Line 14] linting json" not in status.getvalue()
    assert "[Line 18] linting yaml" not in status.getvalue()
    assert "[Line 26] linting yaml" not in status.getvalue()
    assert "[Line 34] linting json" not in status.getvalue()
    assert "[Line 38] linting" not in status.getvalue()


@pytest.mark.sphinx(
    "dummy",
    confoverrides={
        "extensions": ["sphinxawesome.codelinter"],
        "codelinter_languages": {"json": "python -m json.tool"},
    },
)
def test_dummy_compiles_with_codelinter_languages(
    app: Sphinx, status: StringIO
) -> None:
    """It compiles with the dummy builder with configured codelinter_languages."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "[Line 6] linting json" not in status.getvalue()
    assert "[Line 10] linting" not in status.getvalue()
    assert "[Line 14] linting json" not in status.getvalue()
    assert "[Line 18] linting yaml" not in status.getvalue()
    assert "[Line 26] linting yaml" not in status.getvalue()
    assert "[Line 34] linting json" not in status.getvalue()
    assert "[Line 38] linting" not in status.getvalue()


@pytest.mark.sphinx(
    "codelinter",
    confoverrides={
        "extensions": ["sphinxawesome.codelinter"],
        "codelinter_languages": {"json": "does not exist"},
    },
)
def test_codelinter_raises_warning_on_non_existing_tool(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It raises a warning for a non-existing linter."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "does not exist" in warning.getvalue()


@pytest.mark.sphinx(
    "codelinter",
    confoverrides={
        "extensions": ["sphinxawesome.codelinter"],
        "codelinter_languages": {"json": "python -m json.tool"},
    },
)
def test_codelinter_lints_json(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It lints JSON code blocks."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "[Line 6] linting json" in status.getvalue()
    assert "[Line 10] linting" not in status.getvalue()
    assert "[Line 14] linting json" in status.getvalue()
    assert "[Line 18] linting yaml" not in status.getvalue()
    assert "[Line 26] linting yaml" not in status.getvalue()
    assert "[Line 34] linting json" in status.getvalue()
    assert "[Line 38] linting" not in status.getvalue()
    assert "Problem in json" in warning.getvalue()


@pytest.mark.sphinx(
    "codelinter",
    confoverrides={
        "extensions": ["sphinxawesome.codelinter"],
        "codelinter_languages": {"yaml": "yamllint -"},
    },
)
def test_codelinter_lints_yaml(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It lints YAML code blocks."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "[Line 6] linting json" not in status.getvalue()
    assert "[Line 10] linting" not in status.getvalue()
    assert "[Line 14] linting json" not in status.getvalue()
    assert "[Line 18] linting yaml" in status.getvalue()
    assert "[Line 26] linting yaml" in status.getvalue()
    assert "[Line 34] linting json" not in status.getvalue()
    assert "[Line 38] linting" not in status.getvalue()
    assert "Problem in yaml" in warning.getvalue()


@pytest.mark.sphinx(
    "codelinter",
    srcdir="example",
    confoverrides={
        "extensions": ["sphinxawesome.codelinter"],
        "codelinter_languages": {"yaml": "yamllint -", "json": "python -m json.tool"},
    },
)
def test_codelinter_lints_json_and_yaml(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It lints both JSON and YAML code blocks."""
    if app.builder is not None:
        app.builder.build_all()

    assert os.path.exists(app.outdir)
    assert not os.listdir(app.outdir)
    assert "[Line 6] linting json" in status.getvalue()
    assert "[Line 10] linting" not in status.getvalue()
    assert "[Line 14] linting json" in status.getvalue()
    assert "[Line 18] linting yaml" in status.getvalue()
    assert "[Line 26] linting yaml" in status.getvalue()
    assert "[Line 34] linting json" in status.getvalue()
    assert "[Line 38] linting" not in status.getvalue()
    assert "Problem in yaml" in warning.getvalue()
    assert "Problem in json" in warning.getvalue()
