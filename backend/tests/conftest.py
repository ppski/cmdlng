import pytest  # noqa: F401
import requests

from words.lookup import WordLookUp


@pytest.fixture(scope="session")
def lookup_chien():
    return WordLookUp("chiens", "chien")


@pytest.fixture(scope="session")
def lookup_test():
    return WordLookUp("tests", "test")


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


@pytest.fixture
def mock_requests_get_lexicala(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(
            200,
            {
                "n_results": 2,
                "results": [
                    {
                        "headword": {"text": "test", "pos": "noun"},
                        "senses": [{"definition": "test definition"}],
                    }
                ],
            },
        )

    monkeypatch.setattr(requests, "get", mock_get)
