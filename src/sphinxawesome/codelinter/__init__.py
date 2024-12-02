"""Lint code blocks.

Use a ``subprocess.Pipe`` to pipe the code block into a pre-defined program.
This is inherently unsafe, as arbitrary code could be passed to a shell
for execution. But it's flexible and simple.

The implementation mimicks ``cat codeblock | some_tool``.

This was primarily designed (and tested) for linting YAML or JSON code blocks.

:copyright: Copyright 2020, Kai Welke.
:license: MIT, see LICENSE for details
"""

from __future__ import annotations

from collections.abc import Iterable, Set
from importlib.metadata import PackageNotFoundError, version
from io import BytesIO
from subprocess import PIPE, STDOUT, Popen
from typing import Any

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.console import darkgreen, red
from sphinx.util.nodes import get_node_line

logger = logging.getLogger(__name__)

try:
    # Get the version from the package.
    # but the package is ``sphinxawesome-codelinter``,
    # however this module is ``sphinxawesome.codelinter``
    __version__ = version(__name__.replace(".", "-"))
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


class CodeLinter(Builder):
    """Iterate over all ``literal_block`` nodes.

    pipe them into any command line tool that
    can read from standard input.
    """

    name = "codelinter"
    epilog = __("Lint code blocks.")
    allow_parallel = True

    def init(self) -> None:
        """Initialize."""
        pass

    def get_outdated_docs(self) -> str | Iterable[str]:
        """Check for outdated files.

        Return an iterable of outdated output files, or a string describing what an
        update will build.
        """
        return self.env.found_docs  # pragma: nocover

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        """Return Target URI for a document name."""
        return ""  # pragma: nocover

    def prepare_writing(self, docnames: Set[str]) -> None:
        """Run these steps before documents are written."""
        return

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        """Execute the builder."""
        # Read the dict ``codelinter_languages`` from ``conf.py``
        # it has the language as key and the tool as value.
        code_lang = self.app.config.codelinter_languages

        for code in doctree.findall(nodes.literal_block):
            if code["language"] in code_lang:
                line_no = get_node_line(code)
                logger.info(
                    "[Line %d] linting %s ", line_no, code["language"], nonl=True
                )
                io_obj = BytesIO(code.astext().encode())
                # subprocess likes the input as list
                cmd = code_lang[code["language"]].split()
                logger.debug(cmd)
                logger.debug(code.astext())
                try:
                    pipe = Popen(
                        cmd,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=STDOUT,
                    )
                    out, _ = pipe.communicate(input=io_obj.read())
                except FileNotFoundError:
                    logger.error(
                        "command: %s does not exist!", code_lang[code["language"]]
                    )
                    continue

                logger.info(" ")
                if pipe.returncode != 0:
                    logger.warning(red(f'Problem in {code["language"]}: '), nonl=True)
                    logger.warning(out.decode())
                else:
                    logger.info(" " + darkgreen("OK"))

    def finish(self) -> None:
        """Finish the build process."""
        pass


def setup(app: Sphinx) -> dict[str, Any]:
    """Register this extension with Sphinx."""
    app.add_builder(CodeLinter)
    app.add_config_value("codelinter_languages", {}, "env")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
