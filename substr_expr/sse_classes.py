class Key:
    def __init__(self, key: str = "",
                 entries: int = -1) -> None:
        self.key: str = key
        self.entries: int = entries

    def decrease_entries(self) -> None:
        self.entries -= 1