import importlib, pytest
assert importlib.import_module('soulboot').boot() is True
