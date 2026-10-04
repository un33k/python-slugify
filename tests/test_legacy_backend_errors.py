"""Exercise error contracts of the frozen API without altering legacy code."""
import importlib
from unittest.mock import patch
import pytest
from slugify import slugify

legacy = importlib.import_module('slugify._legacy')

def test_legacy_rejects_non_text_input():
    with pytest.raises(TypeError, match='text must be str, bytes or bytearray'):
        slugify(123)

def test_auto_propagates_missing_transitive_dependency():
    error = ModuleNotFoundError("No module named 'internal_dependency'", name='internal_dependency')
    with patch.object(legacy, 'import_module', side_effect=error):
        with pytest.raises(ModuleNotFoundError) as raised:
            slugify('café', backend='auto')
    assert raised.value is error

def test_explicit_backend_is_imported_without_fallback():
    class Backend:
        @staticmethod
        def unidecode(text):
            assert text == 'cafe\u0301'
            return 'cafe'
    with patch.object(legacy, 'import_module', return_value=Backend) as load:
        assert slugify('café', backend='text-unidecode') == 'cafe'
    load.assert_called_once_with('text_unidecode')
