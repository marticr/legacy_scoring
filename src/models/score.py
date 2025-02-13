from dataclasses import dataclass

@dataclass
class Score:
    technique: float
    choreography: float
    performance: float
    expression: float
    jury_member: int
    participant_id: int

    @property
    def total(self) -> float:
        return self.technique + self.choreography + self.performance + self.expression 