import pytest  # noqa: F401


def test_look_up_lexicala(lookup_test, mock_requests_get_lexicala):
    lookup_test.lang_prefix = "fr"
    lookup_test_results = lookup_test.look_up_lexicala()

    assert lookup_test_results is not None
    assert lookup_test_results[0]["pos"] == "NOUN"
    assert lookup_test_results[0]["definition"] == "test definition"
    assert lookup_test_results[0]["source"] == "http://lexicala.com/"
