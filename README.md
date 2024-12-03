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
