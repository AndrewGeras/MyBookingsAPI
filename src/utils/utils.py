from json import load


def read_file(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as file:
        data = load(file)
    return data
