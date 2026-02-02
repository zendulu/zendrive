import json
from pathlib import Path
import pytest

DATA_DIR = Path("pacenotes")

def json_files():
    return list(DATA_DIR.glob("*.json"))


def parametrize_json_files(test_func):
    return pytest.mark.parametrize(
        "json_file",
        json_files(),
        ids=lambda p: p.name,
    )(test_func)


@parametrize_json_files
def test_json_is_valid(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        json.load(f)


@parametrize_json_files
def test_entry_format(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        entries = json.load(f)

    assert isinstance(entries, list), "Top-level JSON must be a list"

    for entry in entries:
        assert isinstance(entry, list), "Each entry must be a list"
        assert len(entry) in (2, 3), "Each entry must have 2 or 3 elements"

        # position 0: integer
        assert isinstance(entry[0], int), "Position 0 must be an integer"

        # position 1: list of strings
        assert isinstance(entry[1], list), "Position 1 must be a list"
        assert all(isinstance(s, str) for s in entry[1]), \
            "All elements in position 1 must be strings"

        # position 2 (optional): dict
        if len(entry) == 3:
            assert isinstance(entry[2], dict), "Position 2 must be a dictionary"


@parametrize_json_files
def test_exactly_one_zero_entry(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        entries = json.load(f)

    zeros = [entry for entry in entries if entry[0] == 0]
    assert len(zeros) == 1, "There must be exactly one entry with 0 in position 0"

@parametrize_json_files
def test_zero_entry_format(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for entry in entries:
        if entry[0] == 0:
            assert entry[1][0] == "starts", \
            'First entry must start with "starts"'

            assert entry[1][-1] == "good luck", \
            'First entry must end with with "good luck"'

@parametrize_json_files
def test_no_negative_values(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for entry in entries:
        assert entry[0] >= 0, "Negative values in position 0 are not allowed"

