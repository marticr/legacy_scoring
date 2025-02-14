from dataclasses import dataclass

@dataclass
class Score:
    participant_id: int  # start_number
    jury_id: int
    technique: int
    choreography: int
    performance: int
    expression: int
    total: float

    @property
    def total(self) -> float:
        return self.technique + self.choreography + self.performance + self.expression 