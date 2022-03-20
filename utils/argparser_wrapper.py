from __future__ import annotations

from argparse import ArgumentParser
from typing import Sequence, Any


class ArgParserWrapper(ArgumentParser):
    def __init__(self, description: str) -> None:
        self.names = []
        super().__init__(description=description)

    def add_arg(self, name: str, arg_type: type) -> ArgParserWrapper:
        self.add_argument(name, type=arg_type)
        self.names.append(name)
        return self

    def parse(self) -> Sequence[Any]:
        parsed_args = self.parse_args()
        return [getattr(parsed_args, name) for name in self.names]
