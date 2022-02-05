from typing import Type

from dataclasses_json import DataClassJsonMixin

from utils.generic_utils import T
from utils.os_utils import write_text_file


class EncodeableJson(DataClassJsonMixin):
    def encode_json(self, path: str) -> None:
        write_text_file(path, self.to_json())

    @classmethod
    def decode_json(cls: Type[T], path: str) -> T:
        with open(path, 'r') as file:
            return cls.from_json(file.read())
