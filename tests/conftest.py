import json

import pytest

# samples : dict[str, dict[str, str]] = { "arms" : { "1": "germany sells arms to saudi arabia", "2": "arms bend at the elbow", "3": "wave your arms around" }


@pytest.fixture
def samples() -> dict[str, dict[str, str]]:
    with open("sentences.json", encoding="utf-8") as fp:
        return json.load(fp)
