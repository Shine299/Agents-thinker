"""en.json and es.json must have exactly the same key set. A mismatch is a
test failure, not a warning (docs/I18N_POLICY.md, section 3).
"""

import json
from pathlib import Path

I18N_DIR = Path(__file__).resolve().parent.parent.parent / "extension" / "i18n"


def load_keys(filename: str) -> set:
    data = json.loads((I18N_DIR / filename).read_text())
    return set(data.keys())


def test_en_and_es_have_identical_keys():
    en_keys = load_keys("en.json")
    es_keys = load_keys("es.json")

    only_in_en = en_keys - es_keys
    only_in_es = es_keys - en_keys

    assert not only_in_en, f"Keys in en.json missing from es.json: {only_in_en}"
    assert not only_in_es, f"Keys in es.json missing from en.json: {only_in_es}"
