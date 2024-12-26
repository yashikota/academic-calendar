import json
import os
import unicodedata


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).replace("\n", " ")


def output_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
