import json
from typing import Any


def write_text_file(path: str, content: str) -> None:
    with open(path, 'w') as file:
        file.write(content)


def read_text_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def decode_json(path: str) -> Any:
    with open(path, 'w') as file:
        return json.load(file)


def encode_json(path: str, obj: Any) -> None:
    with open(path, 'w') as file:
        json.dump(obj, file)
