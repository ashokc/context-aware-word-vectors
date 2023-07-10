import json

import pytest


@pytest.fixture
def samples() -> dict[str, dict[str, str]]:
    with open("sentences.json", encoding="utf-8") as fp:
        return json.load(fp)
