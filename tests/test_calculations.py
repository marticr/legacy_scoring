import pytest
from src.utils.calculations import calculate_average_score, resolve_ex_aequo
from src.models.score import Score

def test_calculate_average_score():
    scores = [
        Score(technique=25, choreography=25, performance=25, expression=8, jury_member=1, participant_id=1),
        Score(technique=28, choreography=27, performance=26, expression=9, jury_member=2, participant_id=1),
        Score(technique=26, choreography=26, performance=27, expression=8, jury_member=3, participant_id=1),
        Score(technique=27, choreography=28, performance=25, expression=9, jury_member=4, participant_id=1)
    ]
    
    average = calculate_average_score(scores)
    assert 80 <= average <= 90  # Expected range for these scores

def test_resolve_ex_aequo():
    scores1 = [
        Score(technique=30, choreography=25, performance=25, expression=8, jury_member=1, participant_id=1),
        Score(technique=30, choreography=27, performance=26, expression=9, jury_member=2, participant_id=1)
    ]
    
    scores2 = [
        Score(technique=28, choreography=28, performance=25, expression=8, jury_member=1, participant_id=2),
        Score(technique=28, choreography=27, performance=26, expression=9, jury_member=2, participant_id=2)
    ]
    
    # scores1 should win due to higher technique score
    assert resolve_ex_aequo(scores1, scores2) == 1 