from __future__ import annotations

from dataclasses import dataclass

from typing import Any


@dataclass
class CsvWriter:
    path: str
    header: List[Any]
    separator: str = ','

    def __enter__(self) -> OpenedCsvWriter:
        opened_file = open(self.path, 'w')
        self.opened_csv_writer = OpenedCsvWriter(opened_file, self.header, self.separator)
        return self.opened_csv_writer

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.opened_csv_writer.close()


@dataclass
class OpenedCsvWriter:
    def __init__(self, file: TextIO, header: List[Any], separator: str) -> None:
        self.file = file
        self.header = header
        self.separator = separator
        self.write_line(*header)

    def write_line(self, *values: Any) -> None:
        assert len(values) == len(self.header),\
            f"CSV Header has {len(self.header)} entries, but {len(values)} are given"
        self.file.write(self.separator.join(map(str, values)))
        self.file.write('\n')

    def close(self) -> None:
        self.file.close()
