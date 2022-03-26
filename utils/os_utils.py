import json
import os
import pickle
import shutil
from typing import Any, Iterable, Tuple


def write_text_file(path: str, content: str) -> None:
    with open(path, 'w') as file:
        file.write(content)


def append_line_text_file(path: str, content: Any) -> None:
    with open(path, 'a') as file:
        file.write(f'{content}\n')
        file.flush()


def read_text_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def decode_json(path: str) -> Any:
    with open(path, 'w') as file:
        return json.load(file)


def encode_json(path: str, obj: Any) -> None:
    with open(path, 'w') as file:
        json.dump(obj, file)


def decode_pickle(path: str) -> Any:
    with open(path, 'rb') as file:
        return pickle.load(file)


def encode_pickle(path: str, obj: Any) -> str:
    with open(path, 'wb') as file:
        pickle.dump(obj, file)
        return path


def join_create_dir(*paths: str, override: bool = False) -> str:
    joined_path = os.path.join(*paths)
    if os.path.exists(joined_path) and override:
        shutil.rmtree(joined_path)
    os.makedirs(joined_path, exist_ok=True)
    return joined_path


def iterate_inner_directories(base_directory: str) -> Iterable[Tuple[str, str]]:
    for dir_name in os.listdir(base_directory):
        dir_path = os.path.join(base_directory, dir_name)
        if os.path.isdir(dir_path):
            yield dir_name, dir_path
