Sphinx Awesome Codelinter
=========================

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An extension for the Sphinx documentation suite to iterate over code blocks
and expose them to an external tool. For example, it is possible to check, if
all JSON code blocks are valid JSON. This ensures, that copied and pasted code
blocks work as expected.

This extension provides a new builder, `sphinx-build -b codelinter`.


Installation
------------

Install the extension:

```console
pip install sphinxawesome-codelinter
```

This Sphinx extension should work with Python versions newer than 3.6 and
recent Sphinx releases.  Unit tests are being run against Python 3.6, 3.7, 3.8
and Sphinx 2.0, 2.1, 2.2, and 2.3.

Configuration
-------------

To enable this extension in Sphinx, add it to the list of extensions:

```python
extensions = ['sphinxawesome.codelinter']
```

The extension is configured via the `codelinter_languages` dictionary, which
is empty by default. That is, no code blocks will be processed unless you
provide the language and the tool to process the language as key, value pair.
For example, to pass all JSON blocks to the python builtin JSON tools, use:

```python
codelinter_languages = {
  'json': 'python -m json.tool'
}
```

which would return an error on non-valid JSON code. For linting YAML code
blocks, you could install the `yamllint` tool and then add:

```python
codelinter_languages = {
  'yaml': 'yamllint -'
}
```

The `-` tells yamllint to read from `stdin`. You can also write your own
tools, that can read from `stdin` and write to `stdout` or `stderr`. The only 
expectation is that any tools retun a value of 0, ifcno errors were found, 
a non-zero value otherwise.

After configuring the extension, you can use `sphinx-build -b codelinter ...`
like other Sphinx builders. No output will be written to disk. If the linter
exits with a non-zero return value, a warning will be logged. You can use the
`sphinx-build -W` option to turn those warnings into errors to stop the build
process.

You can use any reStructuredText directive, that gets parsed as a
`literal_block` node. For example, you can use `.. code-block:: json` as well
as `.. highlight:: json`. 

You can also use the `..literalinclude:: <filename>` directive, to include
code from files. 

```
.. literalinclude:: code.json
   :language: json
```

**Caution:** The value of the `codelinter_languages` dictionary will be used as
provided. No additional safe-guards are in place to prevent abuse.
