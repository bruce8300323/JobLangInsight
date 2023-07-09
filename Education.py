class Education:
    id = None
    degree: str

    def __init__(self, id, degree: str) -> None:
        self.id = id
        self.degree = degree

    def __str__(self) -> str:
        return f"{self.id}, {self.degree}"