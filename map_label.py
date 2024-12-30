class MapLabel():
    def __init__(self, x: int, y: int, text: str, importance: int = 3, style: str = None):
        self.x: int = x
        self.y: int = y
        self.text: str = text
        self.importance: int = importance
        self.style: str = style

    def get_text(self) -> str:
        if self.style in ("City", "Capital"):
            return self.text.upper()
        else:
            return self.text

    def get_font_size(self) -> int:
        return 5 + self.importance

    def get_italics(self) -> bool:
        return (self.style == "Geography")

    def get_icon_metrics(self) -> tuple[int]:
        return (self.x - (self.importance + 3) // 2, self.y - (self.importance + 3) // 2,
                self.importance + 3, self.importance + 3)
