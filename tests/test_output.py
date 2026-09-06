"""Tests for .steam filename + write helpers (Phase 6).

Currently skipped until Phase 6 implementation.
"""

import pytest

from vent.output.write import sanitize_name, steam_filename


@pytest.mark.skip(reason="Phase 6")
def test_sanitize_colons_and_whitespace() -> None:
    assert (
        sanitize_name("Counter-Strike: Global Offensive")
        == "Counter-Strike-Global-Offensive"
    )


@pytest.mark.skip(reason="Phase 6")
def test_steam_filename_extension() -> None:
    assert steam_filename("Terraia") == "Terraia.steam"


@pytest.mark.skip(reason="Phase 6")
def test_sanitize_repeats_and_trim() -> None:
    assert sanitize_name("   A     :    B       ") == "A-B"
