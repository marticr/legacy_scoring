from dataclasses import dataclass
from typing import List
from .category import AgeGroup, Style, Category
from itertools import count

@dataclass
class Participant:
    start_number: int
    name: str
    style: Style
    category: Category
    age_group: AgeGroup

    @classmethod
    def from_csv_line(cls, line: str) -> 'Participant':
        style, category, age_group, start_number, name = line.strip().split(',')
        if not start_number.strip():
            raise ValueError("Start number is mandatory - it determines performance order")
        return cls(
            start_number=int(start_number),
            name=name.strip(),
            style=Style(style.strip()),
            category=Category(category.strip()),
            age_group=AgeGroup(age_group.strip())
        )

    @classmethod
    def load_participants(cls, file_path: str) -> List['Participant']:
        participants = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    participants.append(cls.from_csv_line(line))
        
        # Sort by the hierarchical order
        return sorted(participants, key=lambda p: (
            p.style.value,  # Modern first, then Urban
            [ag.value for ag in AgeGroup].index(p.age_group.value),  # Age group order
            [c.value for c in Category].index(p.category.value),  # Category order
            p.start_number  # Finally by ID
        )) 