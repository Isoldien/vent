"""Tests for .steam filename + write helpers (Phase 6)."""

from vent.output.write import sanitize_name, steam_filename


def test_sanitize_colons_and_whitespace() -> None:
    assert (
        sanitize_name("Counter-Strike: Global Offensive")
        == "Counter-Strike-Global-Offensive"
    )


def test_steam_filename_extension() -> None:
    assert steam_filename("Terraia") == "Terraia.steam"


def test_sanitize_repeats_and_trim() -> None:
    assert sanitize_name("   A     :    B       ") == "A-B"


def test_sanitize_slashes() -> None:
    assert sanitize_name("Fate/Stay Night") == "Fate-Stay-Night"
    assert steam_filename("Fate/Stay Night") == "Fate-Stay-Night.steam"
