from argparse import ArgumentParser, Namespace


class ArgParserWrapper(ArgumentParser):
    def __init__(self, description: str) -> None:
        super().__init__(description=description)

    def add_arg(self, name: str, arg_type: type) -> 'ArgParserWrapper':
        self.add_argument(name, type=arg_type)
        return self

    def parse(self) -> Namespace:
        return self.parse_args()
