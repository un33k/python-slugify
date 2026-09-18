"""Regression test for add_uppercase_char error handling.

Tests that add_uppercase_char either completes atomically or leaves
the input list unchanged on error.
"""
from __future__ import annotations

import pytest
from slugify.special import add_uppercase_char


class TestAddUppercaseCharAtomicity:

    def test_list_unmodified_on_unpack_error(self) -> None:
        """Input list should remain unchanged when unpack fails.

        Before fix: the list was partially modified with items inserted
        before the failing element, leaving state inconsistent.
        """
        # Create list with malformed second element
        original = [('a', 'b')]
        original.append(('bad',))  # type: ignore[arg-type]  # malformed - only 1 element

        with pytest.raises(ValueError):
            add_uppercase_char(original)  # malformed data triggers ValueError

        # After fix: the first valid item should NOT have been processed
        # Before fix: original would be [('A', 'B'), ('a', 'b'), ('bad',)]
        assert original == [('a', 'b'), ('bad',)], (
            f"List should remain unmodified on error, got {original}"
        )

    def test_successful_processing_modifies_list(self) -> None:
        """Verify normal operation still modifies list in place."""
        original = [('x', 'y')]
        result = add_uppercase_char(original)

        # Should add uppercase version at position 0
        assert result == [('X', 'Y'), ('x', 'y')]
        assert original is result  # same object

    def test_empty_list_returns_empty(self) -> None:
        """Empty list is valid and returns empty list."""
        empty: list[tuple[str, str]] = []
        result = add_uppercase_char(empty)

        assert result == []
        assert empty == []
