class Skill:
    id = None
    name: str
    alias: set[str]

    def __init__(self, id, name: str, alias: set = None) -> None:
        self.id = id
        self.name = name
        self.alias = set() if alias == None else alias

    def __str__(self) -> str:
        return f"{self.id}, {self.name}, {','.join(self.alias)}"