import pytest  # noqa: F401


def test_clean_lookup_pos(lookup_chien):
    pos = lookup_chien.clean_lookup_pos("nm")
    assert pos == "NOUN"
