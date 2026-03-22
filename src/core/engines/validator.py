import re
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

from ..data_loader import DataLoader
from ..analyzer import RawDataAnalyzer

@dataclass
class ValidationResult:
    """Structured result of insight validation."""
    status: str  # 'valid', 'invalid', 'error'
    metric: str
    claimed_value: float
    actual_value: float
    error_margin: float
    confidence: float
    explanation: str

class Validator:
    """Engine for validating insight claims against data."""

    def __init__(self, data_loader: DataLoader, analyzer: RawDataAnalyzer):
        self.data_loader = data_loader
        self.analyzer = analyzer

    def validate_insight(self, insight_text: str, dataset_name: str,
                        date_col: str = 'date', tolerance_pct: float = 5.0) -> ValidationResult:
        """Validate an insight claim against loaded data."""
        parse_result = self._parse_insight_text(insight_text)
        if not parse_result:
            return ValidationResult(
                status='error',
                metric='',
                claimed_value=0.0,
                actual_value=0.0,
                error_margin=0.0,
                confidence=0.0,
                explanation='Could not parse insight text'
            )

        metric, claimed_change = parse_result

        data = self.data_loader.get_dataframe(dataset_name)
        if data is None:
            return ValidationResult(
                status='error',
                metric=metric,
                claimed_value=claimed_change,
                actual_value=0.0,
                error_margin=0.0,
                confidence=0.0,
                explanation=f"Dataset '{dataset_name}' not found"
            )

        actual_change = self._calculate_actual_change(data, metric, date_col)
        if actual_change is None:
            return ValidationResult(
                status='error',
                metric=metric,
                claimed_value=claimed_change,
                actual_value=0.0,
                error_margin=0.0,
                confidence=0.0,
                explanation=f"Could not calculate actual change for metric '{metric}'"
            )

        error_margin = abs(actual_change - claimed_change)
        confidence = self._calculate_confidence(error_margin, tolerance_pct)
        status = 'valid' if error_margin <= tolerance_pct else 'invalid'

        explanation = (
            f"Claimed {claimed_change:+.1f}% change, actual {actual_change:+.1f}% change. "
            f"Error margin {error_margin:.1f}% (tolerance {tolerance_pct:.1f}%)"
        )

        return ValidationResult(
            status=status,
            metric=metric,
            claimed_value=claimed_change,
            actual_value=actual_change,
            error_margin=error_margin,
            confidence=confidence,
            explanation=explanation
        )

    def _parse_insight_text(self, text: str) -> Optional[Tuple[str, float]]:
        """Extract metric and claimed percentage change from human insight text."""
        normalized = text.lower().strip()

        patterns = [
            r'(?P<metric>\w+)\s+(?P<dir>dropped|decreased|fell|declined)\s+(?:by\s+)?(?P<value>\d+(?:\.\d+)?)%',
            r'(?P<metric>\w+)\s+(?P<dir>increased|rose|grew|improved)\s+(?:by\s+)?(?P<value>\d+(?:\.\d+)?)%',
            r'(?P<metric>\w+)\s+changed\s+(?:by\s+)?(?P<value>-?\d+(?:\.\d+)?)%'
        ]

        for pattern in patterns:
            m = re.search(pattern, normalized)
            if m:
                metric = m.group('metric')
                value = float(m.group('value'))
                direction = m.groupdict().get('dir')

                if direction in ['dropped', 'decreased', 'fell', 'declined']:
                    value = -abs(value)
                elif direction in ['increased', 'rose', 'grew', 'improved']:
                    value = abs(value)

                return metric, value

        # fallback: explicit positive/negative
        m = re.search(r'(?P<metric>\w+)\s+(?:is\s+)?(?P<value>-?\d+(?:\.\d+)?)%', normalized)
        if m:
            return m.group('metric'), float(m.group('value'))

        return None

    def _calculate_actual_change(self, data: pd.DataFrame, metric: str, date_col: str) -> Optional[float]:
        if metric not in data.columns:
            return None

        try:
            pct_series = self.analyzer.percentage_change(data, date_col, metric, periods=1)
            if pct_series.empty:
                return None
            return float(pct_series.dropna().iloc[-1])
        except Exception:
            return None

    def _calculate_confidence(self, error_margin: float, tolerance: float) -> float:
        base = max(0.0, 1.0 - (error_margin / max(tolerance, 1.0)))
        return round(min(1.0, max(0.0, base)), 2)
