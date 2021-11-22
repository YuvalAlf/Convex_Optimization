from dataclasses import dataclass


@dataclass
class TabPrinter:
    debug: bool
    tabs = 0

    def __enter__(self):
        self.tabs += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.tabs > 0
        self.tabs -= 1

    def tab_print(self, string: str):
        if self.debug:
            print('\t' * self.tabs + string)

    def regular_print(self, string: str):
        if self.debug:
            print('\t' * (self.tabs - 1) + string)
            assert self.tabs > 0
