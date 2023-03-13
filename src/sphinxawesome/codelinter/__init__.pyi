from typing import Any, Iterable

from _typeshed import Incomplete
from docutils import nodes
from sphinx.application import Sphinx as Sphinx
from sphinx.builders import Builder

logger: Incomplete
__version__: str

class CodeLinter(Builder):
    name: str
    epilog: Incomplete
    allow_parallel: bool
    def init(self: CodeLinter) -> None: ...
    def get_outdated_docs(self: CodeLinter) -> str | Iterable[str]: ...
    def get_target_uri(
        self: CodeLinter, docname: str, typ: str | None = ...
    ) -> str: ...
    def prepare_writing(self: CodeLinter, docnames: set[str]) -> None: ...
    def write_doc(self: CodeLinter, docname: str, doctree: nodes.Node) -> None: ...
    def finish(self: CodeLinter) -> None: ...

def setup(app: Sphinx) -> dict[str, Any]: ...