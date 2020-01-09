import os
import pytest
from sphinxawesome.codelinter import __version__


def test_version():
    '''test that the version we expect is indeed here.'''

    assert __version__ == '0.1.0'


def test_rootdir_fixture(rootdir):
    '''
    Test basic assumptions about test files/directories.
    The test files are in './example/test-root'. I haven't found a way yet to
    tell pytest/sphinx that I do not want an extra nesting level here.
    '''

    conf_file = rootdir / 'test-root' / 'conf.py'
    index_file = rootdir / 'test-root' / 'index.rst'
    assert 'example' in rootdir
    assert conf_file.exists()
    assert index_file.exists()


@pytest.mark.sphinx('dummy', srcdir='example')
def test_basic_config(app):
    '''
    Test a basic compilation of a minimal configuration.
    We use the `dummy` builder, so no output is expected.
    '''

    app.builder.build_all()
    assert app.outdir.exists()
    assert not os.listdir(app.outdir)


@pytest.mark.sphinx('dummy', srcdir='example',
                    confoverrides={'extensions': ['sphinxawesome.codelinter']})
def test_extension_enabled(app):
    '''
    Test enabling the extension without configuring it to run.
    '''

    app.builder.build_all()
    assert app.outdir.exists()
    assert not os.listdir(app.outdir)
    assert 'codelinter_languages' in app.config


@pytest.mark.sphinx('codelinter', srcdir='example',
                    confoverrides={'extensions': ['sphinxawesome.codelinter']})
def test_codelinter_empty(app, status):
    '''
    Test the codelinter builder without any configuration.
    '''

    app.builder.build_all()
    assert app.outdir.exists()
    assert not os.listdir(app.outdir)
    assert 'codelinter_languages' in app.config
    assert '[Line 6] linting json' not in status.getvalue()
    assert '[Line 10] linting' not in status.getvalue()
    assert '[Line 14] linting json' not in status.getvalue()
    assert '[Line 18] linting yaml' not in status.getvalue()
    assert '[Line 26] linting yaml' not in status.getvalue()


@pytest.mark.sphinx('dummy', srcdir='example',
                    confoverrides={
                        'extensions': ['sphinxawesome.codelinter'],
                        'codelinter_languages': {'json': 'python -m json.tool'}
                    })
def test_dummy_configured(app, status):
    '''
    Test normal builder with configured codelinter_languages dict.
    '''

    app.builder.build_all()
    assert app.outdir.exists()
    assert not os.listdir(app.outdir)
    assert '[Line 6] linting json' not in status.getvalue()
    assert '[Line 10] linting' not in status.getvalue()
    assert '[Line 14] linting json' not in status.getvalue()
    assert '[Line 18] linting yaml' not in status.getvalue()
    assert '[Line 26] linting yaml' not in status.getvalue()


@pytest.mark.sphinx('codelinter', srcdir='example',
                    confoverrides={
                        'extensions': ['sphinxawesome.codelinter'],
                        'codelinter_languages': {'json': 'python -m json.tool'}
                    })
def test_codelinter_json(app, status, warning):
    '''
    Test codelinter builder for JSON code blocks.
    '''

    app.builder.build_all()

    assert app.outdir.exists()
    assert not os.listdir(app.outdir)
    assert '[Line 6] linting json' in status.getvalue()
    assert '[Line 10] linting' not in status.getvalue()
    assert '[Line 14] linting json' in status.getvalue()
    assert '[Line 18] linting yaml' not in status.getvalue()
    assert '[Line 26] linting yaml' not in status.getvalue()
    assert 'Problem in json' in warning.getvalue()


@pytest.mark.sphinx('codelinter', srcdir='example',
                    confoverrides={
                        'extensions': ['sphinxawesome.codelinter'],
                        'codelinter_languages': {'yaml': 'yamllint -'}
                    })
def test_codelinter_yaml(app, status, warning):
    '''
    Test codelinter builder for YAML code blocks.
    '''

    app.builder.build_all()

    assert app.outdir.exists()
    assert not os.listdir(app.outdir)
    assert '[Line 6] linting json' not in status.getvalue()
    assert '[Line 10] linting' not in status.getvalue()
    assert '[Line 14] linting json' not in status.getvalue()
    assert '[Line 18] linting yaml' in status.getvalue()
    assert '[Line 26] linting yaml' in status.getvalue()
    #  assert 'Problem in yaml' in warning.getvalue()
    # TODO: currently yamllint doesn't throw an error. I suspect this has
    # something do to with the way yamllint is being called `yamllint -` and
    # subprocess.PIPE. Further investigations are required here
