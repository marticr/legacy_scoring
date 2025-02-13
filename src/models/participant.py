from dataclasses import dataclass
from .category import AgeGroup, Style, Category

@dataclass
class Participant:
    name: str
    style: Style
    category: Category
    age_group: AgeGroup
    start_number: int 