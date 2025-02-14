from enum import Enum

class AgeGroup(Enum):
    MINI = "mini"
    KIDS = "kids"
    JUNIORS = "juniors"
    TEENS = "teens"
    ADULTS = "adults"

class Style(Enum):
    MODERN = "modern"
    URBAN = "urban"

class Category(Enum):
    SOLO = "solo"
    DUO = "duo"
    TEAMS = "teams" 