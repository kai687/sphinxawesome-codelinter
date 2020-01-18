"""
Lint code blocks.

Use a subprocess.Pipe to pipe the code block into a pre-defined program.
This is inherently unsafe, as arbitrary code could be passed to a shell
for execution.

The implementation mimicks ``cat codeblock | some_tool``.

This was designed for linting YAML or JSON code blocks, but can be abused
in all sort of ways.

:copyright: Copyright 2019, Kai Welke.
:license: MIT, see LICENSE for details
"""

from io import BytesIO
from subprocess import Popen, PIPE, STDOUT
from typing import Dict, Any, Set, Optional
from docutils import nodes
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.nodes import get_node_line
from sphinx.util.console import red, darkgreen
from sphinx.application import Sphinx

logger = logging.getLogger(__name__)

__version__ = "1.0.2"


class CodeLinter(Builder):
    """
    A Builder that iterates over all literal blocks and passes pipes them into
    a tool for post-processing, for example linting.
    """

    name = "codelinter"
    epilog = __("Lint code blocks.")
    allow_parallel = True

    def init(self) -> None:
        pass

    def get_outdated_docs(self) -> Set[str]:
        return self.env.found_docs

    def get_target_uri(self, docname: str, typ: Optional[str] = None) -> str:
        return ""

    def prepare_writing(self, docnames: Set[str]) -> None:
        return

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        """
        ``codelinter_languages`` is a dictionary with the language as key
        and the command to run on the code block as value. This is specified
        in ``conf.py``.

        For example:
            codelinter_languages = {'json': 'python3 -m json.tool'}
            pipes any JSON code block to the JSON module of python.
        """
        code_lang = self.app.config.codelinter_languages

        for code in doctree.traverse(nodes.literal_block):
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
                    pipe = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                    out, err = pipe.communicate(input=io_obj.read())
                except FileNotFoundError:
                    logger.error(
                        f'command: "{code_lang[code["language"]]}" ' "does not exist!"
                    )
                    continue

                logger.info(" ")
                if pipe.returncode != 0:
                    logger.warning(red(f'Problem in {code["language"]}: '), nonl=True)
                    logger.warning(out.decode())
                else:
                    logger.info(" " + darkgreen("OK"))

    def finish(self) -> None:
        pass


def setup(app: Sphinx) -> Dict[str, Any]:
    """register this extension with Sphinx"""
    app.add_builder(CodeLinter)
    app.add_config_value("codelinter_languages", {}, "env")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
