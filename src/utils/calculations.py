from typing import List
from ..models.score import Score

def calculate_average_score(scores: List[Score]) -> float:
    total = sum(score.total for score in scores)
    return total / len(scores)

def resolve_ex_aequo(scores1: List[Score], scores2: List[Score]) -> int:
    """Returns 1 if scores1 wins, -1 if scores2 wins, 0 if truly equal"""
    avg_technique1 = sum(s.technique for s in scores1) / len(scores1)
    avg_technique2 = sum(s.technique for s in scores2) / len(scores2)
    
    if avg_technique1 != avg_technique2:
        return 1 if avg_technique1 > avg_technique2 else -1
        
    avg_performance1 = sum(s.performance for s in scores1) / len(scores1)
    avg_performance2 = sum(s.performance for s in scores2) / len(scores2)
    
    if avg_performance1 != avg_performance2:
        return 1 if avg_performance1 > avg_performance2 else -1
        
    avg_choreography1 = sum(s.choreography for s in scores1) / len(scores1)
    avg_choreography2 = sum(s.choreography for s in scores2) / len(scores2)
    
    if avg_choreography1 != avg_choreography2:
        return 1 if avg_choreography1 > avg_choreography2 else -1
    
    return 0 