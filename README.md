Sphinx Awesome Codelinter
=========================

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An extension for the Sphinx documentation suite to iterate over code blocks
and expose them to an external tool. For example, it is possible to check, if
all JSON code blocks are valid JSON. This ensures, that copied and pasted code
blocks work as expected.

This extension acts like a Sphinx builder, e.g. like the Sphinx linkcheck
builder.


Installation
------------

Install the extension:

```console
pip install sphinxawesome-codelinter
```

Configuration
-------------

To enable this extension in Sphinx, add it to the list of extensions:

```python
extensions = ['sphinxawesome.codelinter']
```

If you want to enable linting for a specific language, configure the
`codelinter_languages` dictionary. For example, to pass all JSON blocks to the
python builtin JSON tools, use:

```python
codelinter_languages = {
  'json': 'python -m json.tool'
}
```

For linting YAML code blocks, you could install the `yamllint` tool and then
add:

```python
codelinter_languages = {
  'yaml': 'yamllint -'
}
```

The `-` tells yamllint to read from `stdin`. After configuring the extension,
you can use `sphinx-build -b codelinter ...` like other Sphinx builders. No
output should be written to disk.

You can use any reStructuredText directive, that gets parsed as a
`literal_block` node. The directives `.. code-block:: json`, `.. highlight::
json` will both work. 

You can also use the `..literalinclude:: <filename>` diggrective, if the
language is specified with the `:language: json` field.
