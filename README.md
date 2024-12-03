# Sphinx awesome codelinter

[![License](https://img.shields.io/github/license/kai687/sphinxawesome-codelinter?color=blue&style=for-the-badge)](https://github.com/kai687/sphinxawesome-codelinter/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/sphinxawesome-codelinter?style=for-the-badge)](https://pypi.org/project/sphinxawesome-codelinter)

The **awesome codelinter** extension for the
[Sphinx documentation generator](https://www.sphinx-doc.org) lets you verify that code blocks are valid or follow a preferred style.
The extension lets you run external tools,
such as linters,
over all code blocks in your Sphinx documentation.

## Install

Install the extension:

```console
pip install sphinxawesome-codelinter
```

Requirements:

- Python >= 3.9
- Sphinx >= 7

## Configure

To use this extension,
add it to the list of extensions in your Sphinx configuration file `conf.py`:

```python
extensions += ["sphinxawesome.codelinter"]
```

To use an external tool to check code blocks,
add the language and tool as key-value pairs to the `codelinter_languages` dictionary.
By default, the dictionary is empty,
so no code blocks will be processed unless added.

For example, to pass all JSON blocks to Python's built-in JSON module, use:

```python
codelinter_languages = {"json": "python -m json.tool"}
```

The Python command `python -m json.tool` returns an error for non-valid JSON code.
To lint YAML code blocks, install the `yamllint` tool and add:

```python
codelinter_languages = {"yaml": "yamllint -"}
```

The `-` tells yamllint to read from `stdin`.
You can write your own tools that read from `stdin` and write to `stdout` or `stderr`.
They should return `0` if no errors are found,
a non-zero value otherwise.

You can use any reStructuredText directive that gets parsed as a `literal_block` node.
For example, you can use `.. code-block:: json`, `.. code:: json`,
or `..literalinclude:: <filename>` to include code from files.

```rst
.. literalinclude:: code.json
   :language: json
```

> [!CAUTION]
> The command you add to the `codelinter_languages` dictionary is called as you provide it.
> No additional safe-guards are in place to prevent abuse.

## Use

Run `sphinx-build -b codelinter` to check your code blocks.
If any tool returns a non-zero value, a warning is logged.
To turn warnings into errors and stop the build process,
use `sphinx-build -W`.

## Bring your own tools

Since the `codelinter_languages` dictionary accepts any program,
you're not limited to existing solutions.

The following example runs a custom linter on Python and C code blocks.
It shows how you can achieve the following tasks:

- Check that Python code passes [`mypy`](https://mypy-lang.org/) checks.
  Mypy doesn't support reading from standard input,
  so you can't use it directly.
- Check that C code can compile without warnings.
- Add C boilerplate code if there's a special comment in the code block.
- Opt out of linting specific code blocks if there's a special comment.

```python
# File: docs/linters.py
import argparse
import subprocess
import sys

python_code_preface = """
import numpy as np
import customlib
"""


def lint_python(code: str) -> None:
    full_code = python_code_preface + code
    if "# no-check" in full_code:  # skip checking
        return
    subprocess.run(["mypy", "-c", f"{full_code}"], check=True)


def lint_c(code: str) -> None:
    if "// no-check" in code:  # skip checking
        return

    # it is a full example
    if "// full" in code:
        full_code = (
            """
#include <stdlib.h>
#include <stdio.h>
"""
            + code
        )
    else:
        full_code = (
            """
#include <stdlib.h>
#include <stdio.h>

int main() {
"""
            + code
            + """
    return 0;
}
"""
        )
    subprocess.run(
        [
            "gcc",
            "-c",
            "-x",
            "c",
            "-Wall",
            "-Werror",
            "-ansi",
            "-std=c99",
            "-pedantic",
            "-pedantic-errors",
            "-Wno-unused-variable",
            "-Wno-unused-but-set-variable",
            "-Wno-unused-local-typedefs",
            "-o",
            "/dev/null",
            "-",
        ],
        input=full_code.encode(),
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("linter", choices=("python", "c"))
    args = parser.parse_args()
    code = sys.stdin.read()

    if args.linter == "python":
        lint_python(code)
    else:
        lint_c(code)


if __name__ == "__main__":
    main()
```

To use this linter, add the following to your Sphinx configuration:

```python
# File: conf.py
codelinter_languages = {
    "python": "python -m docs.linters python",
    "c": "python -m docs.linters c",
}
```
