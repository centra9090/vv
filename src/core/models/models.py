from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class AnalysisResult:
    """Structured output for the Decision Intelligence System."""
    analysis_id: str
    timestamp: str
    insight_input: str
    validation: Dict[str, Any]
    metrics: Dict[str, Any]
    root_cause: Dict[str, Any]
    decision: Dict[str, Any]
    confidence: Dict[str, Any]
    limitations: List[str]
    consistency_checks: List[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]

    @classmethod
    def create(cls, analysis_id: str, insight_input: str) -> 'AnalysisResult':
        """Factory method to create a new AnalysisResult with defaults."""
        return cls(
            analysis_id=analysis_id,
            timestamp=datetime.now().isoformat(),
            insight_input=insight_input,
            validation={},
            metrics={},
            root_cause={},
            decision={},
            confidence={},
            limitations=[],
            consistency_checks=[],
            audit_trail=[]
        )