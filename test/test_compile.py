


def test_compile():
    try:
        import tiddlywebplugins.relativetime
        assert True
    except ImportError, exc:
        assert False, exc
