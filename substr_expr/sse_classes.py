class Keys:
    def __init__(self, keys: str | list[str] = "",
                 entries: int = -1) -> None:
        self.keys: str | list[str] = keys
        self.entries: int = entries