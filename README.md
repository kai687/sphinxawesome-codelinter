Sphinx Awesome Codelinter
=========================

![GitHub](https://img.shields.io/github/license/kai687/sphinxawesome-codelinter?style=flat-square)

Pipe all code blocks into your favorite linter.

This Sphinx extension exposes every `code-block`, `highlight`, and other
literal, which can then be piped into a linter.

The extension is configured with a `codelinter_languages` dictionary. E.g. to
lint all JSON code blocks, use:

```python
codelinter_languages = {
    'json': 'python3 -m json.tool'
}
```
