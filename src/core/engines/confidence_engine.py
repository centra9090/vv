from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from ..utils.helpers import detect_outliers_zscore

class ConfidenceEngine:
    """Engine for assessing confidence in analysis results."""

    def __init__(self):
        pass

    def score_confidence(self, data: pd.DataFrame, metric: str,
                        validation_result: Any, root_cause_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall confidence score for the analysis."""
        confidence_factors = {}

        # Data quality factor
        data_quality = self._assess_data_quality(data, metric)
        confidence_factors['data_quality'] = data_quality

        # Validation strength factor
        validation_strength = self._assess_validation_strength(validation_result)
        confidence_factors['validation_strength'] = validation_strength

        # Root cause clarity factor
        root_cause_clarity = self._assess_root_cause_clarity(root_cause_result)
        confidence_factors['root_cause_clarity'] = root_cause_clarity

        # Sample size factor
        sample_size = self._assess_sample_size(data)
        confidence_factors['sample_size'] = sample_size

        # Calculate weighted overall confidence
        weights = {
            'data_quality': 0.3,
            'validation_strength': 0.3,
            'root_cause_clarity': 0.2,
            'sample_size': 0.2
        }

        overall_confidence = sum(
            confidence_factors[factor] * weights[factor]
            for factor in confidence_factors
        )

        return {
            'overall_confidence': round(overall_confidence, 2),
            'confidence_factors': confidence_factors,
            'confidence_level': self._get_confidence_level(overall_confidence)
        }

    def _assess_data_quality(self, data: pd.DataFrame, metric: str) -> float:
        """Assess data quality (0-1 scale)."""
        quality_score = 1.0

        # Check for missing values in metric
        missing_pct = data[metric].isnull().mean()
        quality_score -= missing_pct * 0.5

        # Check for data consistency (no extreme outliers)
        if len(data) > 10:
            outliers = detect_outliers_zscore(data[metric])
            outlier_pct = outliers.mean()
            quality_score -= outlier_pct * 0.3

        return max(0.0, min(1.0, quality_score))

    def _assess_validation_strength(self, validation_result: Any) -> float:
        """Assess validation result strength (0-1 scale)."""
        if not hasattr(validation_result, 'confidence'):
            return 0.5

        # Use the confidence score from validation
        return getattr(validation_result, 'confidence', 0.5)

    def _assess_root_cause_clarity(self, root_cause_result: Dict[str, Any]) -> float:
        """Assess root cause analysis clarity (0-1 scale)."""
        if 'primary_root_cause' not in root_cause_result:
            return 0.3

        primary = root_cause_result['primary_root_cause']
        if not primary:
            return 0.3

        # Higher confidence if contribution percentage is significant
        contribution = abs(primary.get('contribution_pct', 0))
        if contribution > 50:
            return 0.9
        elif contribution > 25:
            return 0.7
        elif contribution > 10:
            return 0.5
        else:
            return 0.3

    def _assess_sample_size(self, data: pd.DataFrame) -> float:
        """Assess sample size adequacy (0-1 scale)."""
        n = len(data)
        if n >= 1000:
            return 1.0
        elif n >= 100:
            return 0.8
        elif n >= 30:
            return 0.6
        elif n >= 10:
            return 0.4
        else:
            return 0.2

    def _get_confidence_level(self, score: float) -> str:
        """Convert confidence score to descriptive level."""
        if score >= 0.8:
            return 'High'
        elif score >= 0.6:
            return 'Medium'
        elif score >= 0.4:
            return 'Low'
        else:
            return 'Very Low'