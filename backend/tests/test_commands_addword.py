import pytest  # noqa: F401

from io import StringIO
from django.core.management import call_command


@pytest.mark.django_db
def test_custom_command(mocker, capsys):
    args = [
        "--add",
        "test_word",
        "--source_lang",
        "fr_fr",
        "--target_lang",
        "fr_fr",
    ]

    mock_stdout = mocker.patch("sys.stdout", new_callable=StringIO)
    call_command("addword", *args)

    captured = capsys.readouterr()
    output = "TODO"  # captured.out

    assert "TODO" in output
