import os
import pytest
from sphinxawesome.codelinter import __version__

def test_version():
    assert __version__ == '0.1.0'


def test_rootdir_fixture(rootdir):
    '''
    Test basic assumptions about test files/directories.
    The test files are in './example/test-root'. I haven't found a way yet to
    tell pytest/sphinx that I do not want an extra nesting level here.
    '''

    conf_file = rootdir / 'test-root' /  'conf.py'
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


#  @pytest.mark.sphinx('dummy', srcdir='example',
                    #  confoverrides={'extensions': ['sphinxawesome-codelinter']})
#  def test_extension_enabled(app):
    #  '''
    #  We want to test enabling the extension, but not configuring it.
    #  '''

    #  app.builder.build_all()
    #  assert app.outdir.exists()
    #  assert not os.listdir(app.outdir)

# test that enabling the extension leads to a successful compilation
# test that enabling and configuring the extension leads to a successful run
# test that configuring but not enabling the extension throws an error
