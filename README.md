# Sphinx awesome codelinter

[![License](https://img.shields.io/github/license/kai687/sphinxawesome-codelinter?color=blue&style=for-the-badge)](https://github.com/kai687/sphinxawesome-codelinter/blob/master/LICENSE)
[![PyTest Status](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-codelinter/Run%20unit%20tests%20against%20different%20versions%20of%20Python?label=tests&style=for-the-badge)](https://github.com/kai687/sphinxawesome-codelinter/actions?query=workflow%3A%22Run+unit+tests%22)
[![Codecov](https://img.shields.io/codecov/c/gh/kai687/sphinxawesome-codelinter?style=for-the-badge)](https://codecov.io/gh/kai687/sphinxawesome-codelinter)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/sphinxawesome-codelinter?style=for-the-badge)
![Code style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)

This extension for the [Sphinx documentation generator](https://www.sphinx-doc.org) exposes code blocks in your documentation to an external tool.
This can be used to check that code blocks are valid or follow a certain style.

## Installation

Install the extension:

```console
pip install sphinxawesome-codelinter
```

This Sphinx extension works with Python versions newer than 3.6 and recent Sphinx releases.

## Configuration

To enable this extension in Sphinx, add it to the list of extensions in the Sphinx
configuration file `conf.py`:

```python
extensions = ["sphinxawesome.codelinter"]
```

To pass code blocks to an external tool, provide the language as a key and the tool as
the associated value to the `codelinter_languages` dictionary. This dictionary is
initially empty, so even if the extension is installed and included in the `extensions`
list, no code blocks will be processed by default.

For example, to pass all JSON blocks to Python's built-in JSON module, use:

```python
codelinter_languages = {
  "json": "python -m json.tool"
}
```

The Python command `python -m json.tool` returns an error for non-valid JSON code.
For linting YAML code blocks, you could install the `yamllint` tool and add:

```python
codelinter_languages = {
  "yaml": "yamllint -"
}
```

The `-` tells yamllint to read from `stdin`. You can also write your own tools that can
read from `stdin` and write to `stdout` or `stderr`. The only expectation is that any
tools returns a value of 0 if no errors were found, a non-zero value otherwise.

You can use any reStructuredText directive that gets parsed as a `literal_block` node.
For example, you can use `.. code-block:: json` or `.. code:: json` directives.

You can also use the `..literalinclude:: <filename>` directive to include code from
files.

```
.. literalinclude:: code.json
   :language: json
```

> **Caution:** The value of the `codelinter_languages` dictionary will be called as
> provided. No additional safe-guards are in place to prevent abuse.

## Use

The extension exposes a builder in Sphinx. Use `sphinx-build -b codelinter` to run it.
No output is written to disk.
If the codelinter tool exits with a non-zero return value, it logs a warning.
You can use the `sphinx-build -W` option to turn warnings into errors and stop the build process.
