from dataclasses import dataclass
from model.country import Country

@dataclass
class LandContiguity:
    Country1 : Country
    Country2 : Country
    Year: int

    def __hash__(self):
        return hash((self.Country1, self.Country2))

    def __eq__(self, other):
        return self.Country1 == other.Country1 and self.Country2 == other.Country2

    def __str__(self):
        pass