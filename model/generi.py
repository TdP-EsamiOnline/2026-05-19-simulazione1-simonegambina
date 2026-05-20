from dataclasses import dataclass

@dataclass
class Genere:
    genre_id: int
    name: str


    def __hash__(self):
        return self.genre_id

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.genre_id == other.genre_id