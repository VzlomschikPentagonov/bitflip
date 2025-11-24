class Arg:
    def __init__(self, keys: list[str],
                 entries: int = -1) -> None:
        self.keys: list[str] = keys
        self.entries: int = entries

    def decrease_entries(self) -> None:
        self.entries -= 1
