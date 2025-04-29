import importlib
def test_boot():
    sb = importlib.import_module('soulboot')
    assert sb.boot() is True
