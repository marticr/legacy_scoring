from enum import Enum

class AgeGroup(Enum):
    MINI = "Mini"
    KIDS = "Kids"
    JUNIORS = "Juniors"
    TEENS = "Teens"
    ADULTS = "Adults"

class Style(Enum):
    MODERN = "Modern"
    URBAN = "Urban"

class Category(Enum):
    SOLO = "Solo"
    DUO = "Duo"
    TEAMS = "Teams" 