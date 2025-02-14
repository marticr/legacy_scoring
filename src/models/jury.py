from dataclasses import dataclass

@dataclass
class JuryMember:
    id: int
    name: str
    style: str  # "Modern" or "Urban" 