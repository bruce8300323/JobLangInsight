class Category:
    id = None
    name: str

    def __init__(self, id, name: str) -> None:
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return f"{self.id}, {self.name}"