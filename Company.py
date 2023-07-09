class Company:
    id = None
    name: str
    category: str

    def __init__(self, id, name: str, category: str = "") -> None:
        self.id = id
        self.name = name
        self.category = category

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} - {self.category}"