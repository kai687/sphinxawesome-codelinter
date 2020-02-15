# Sphinx Awesome Codelinter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/sphinxawesome-codelinter)](https://img.shields.io/pypi/v/sphinxawesome-codelinter)
[![Test Status](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-codelinter/Run%20unit%20tests%20against%20different%20versions%20of%20Python?label=tests)](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-codelinter/Run%20unit%20tests%20against%20different%20versions%20of%20Python?label=tests)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This extension for the Sphinx documentation generator allows you to expose code blocks
in your documentation to an external tool. This can be used to check that code blocks
contain only valid code. For more information about the Sphinx project, visit the
website at http://www.sphinx-doc.org/.

This extension provides a new builder, `sphinx-build -b codelinter`.

## Installation

Install the extension:

```console
pip install sphinxawesome-codelinter
```

This Sphinx extension should work with Python versions newer than 3.6 and recent Sphinx
releases. The versions against which the unit tests are run is in the file
`.github/workflows/tests.yml` in this repository.

## Configuration

To enable this extension in Sphinx, add it to the list of extensions in the Sphinx
configuration file `conf.py`:

```python
extensions = ['sphinxawesome.codelinter']
```

The extension is configured via the `codelinter_languages` dictionary, which is empty by
default. That is, no code blocks will be processed unless you provide the language and
the tool to process the language as a key/value pair. For example, to pass all JSON
blocks to the python builtin JSON module, use:

```python
codelinter_languages = {
  'json': 'python -m json.tool'
}
```

which returns an error for non-valid JSON code. For linting YAML code blocks, you could
install the `yamllint` tool and then add:

```python
codelinter_languages = {
  'yaml': 'yamllint -'
}
```

The `-` tells yamllint to read from `stdin`. You can also write your own tools, that can
read from `stdin` and write to `stdout` or `stderr`. The only expectation is that any
tools returns a value of 0, if no errors were found, a non-zero value otherwise.

## Use

Use `sphinx-build -b codelinter` like other Sphinx builders. No output will be written
to disk. If the linter exits with a non-zero return value, a warning will be logged. You
can use the `sphinx-build -W` option to turn those warnings into errors to stop the
build process.

You can use any reStructuredText directive, that gets parsed as a `literal_block` node.
For example, you can use `.. code-block:: json` as well as `.. highlight:: json`.

You can also use the `..literalinclude:: <filename>` directive, to include code from
files.

```
.. literalinclude:: code.json
   :language: json
```

**Caution:** The value of the `codelinter_languages` dictionary will be called as
provided. No additional safe-guards are in place to prevent abuse.
