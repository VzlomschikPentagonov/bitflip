class Key:
    def __init__(self, identifier: list[int] | str,
                 keys: list[str],
                 entries: int = -1) -> None:
        self.identifier: list[int] | str = identifier
        self.keys: list[str] = key
        self.entries: int = entries

    def decrease_entries(self) -> None:
        self.entries -= 1
