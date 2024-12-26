import unicodedata


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).replace("\n", " ")
