import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Any

class RawDataAnalyzer:
    """Analyzer for raw data calculations."""

    def statistical_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate a summary of basic data statistics."""
        numeric = data.select_dtypes(include=[np.number])

        return {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.apply(lambda x: x.name).to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'duplicate_rows': int(data.duplicated().sum()),
            'percentage_duplicates': float(data.duplicated().mean() * 100),
            'numeric_summary': numeric.describe().to_dict() if not numeric.empty else {}
        }

    def trend_analysis(self, data: pd.DataFrame, date_col: str, value_col: str, min_points: int = 3) -> Dict[str, Any]:
        """Analyze trend by linear regression on sorted date-value series."""
        if value_col not in data.columns or date_col not in data.columns:
            return {'error': 'Missing required columns for trend analysis'}

        df = data.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, value_col])
        df = df.sort_values(date_col)

        if len(df) < min_points:
            return {'error': 'Not enough data points for trend analysis'}

        x = np.arange(len(df))
        y = df[value_col].astype(float).values

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        trend_direction = 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'

        return {
            'slope': float(slope),
            'intercept': float(intercept),
            'r_squared': float(r_value**2),
            'p_value': float(p_value),
            'std_err': float(std_err),
            'trend_direction': trend_direction,
            'observations': len(df)
        }

    def percentage_change(self, data: pd.DataFrame, date_col: str, value_col: str, periods: int = 1) -> pd.Series:
        """Calculate percentage change over periods and return series with indexing preserved."""
        if date_col not in data.columns or value_col not in data.columns:
            raise KeyError(f"Missing columns: {date_col} or {value_col}")

        df = data.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.sort_values(date_col)

        changes = df[value_col].astype(float).pct_change(periods=periods) * 100
        return changes

    def validate_metric_range(self, data: pd.DataFrame, metric: str, min_val: float, max_val: float) -> Dict[str, Any]:
        """Validate metric values are within min/max bounds."""
        if metric not in data.columns:
            return {
                'valid': False,
                'reason': f"Metric '{metric}' not found",
                'valid_count': 0,
                'total_count': 0,
                'percentage_valid': 0.0
            }

        values = pd.to_numeric(data[metric], errors='coerce')
        valid_mask = values.between(min_val, max_val)
        total_count = int(len(values))
        valid_count = int(valid_mask.sum())

        return {
            'valid': valid_count == total_count,
            'valid_count': valid_count,
            'total_count': total_count,
            'percentage_valid': float(valid_count / total_count * 100) if total_count > 0 else 0.0
        }

    def root_cause_candidates(self, data: pd.DataFrame, target_col: str, group_cols: List[str]) -> pd.DataFrame:
        """Estimate root_cause candidates via group-level contribution and variance."""
        if target_col not in data.columns:
            raise KeyError(f"Target column '{target_col}' missing")

        results = []

        for col in group_cols:
            if col not in data.columns:
                continue
            grouped = data.groupby(col)[target_col].agg(['mean', 'std', 'count', 'sum']).reset_index()
            grouped['variance'] = grouped['std'] ** 2
            grouped['impact_score'] = grouped['mean'] * np.sqrt(grouped['count'])
            grouped['group_by'] = col
            results.append(grouped)

        if not results:
            return pd.DataFrame()

        return pd.concat(results, ignore_index=True)

    def hypothesis_test(self, data: pd.DataFrame, col1: str, col2: str, test_type: str = 't-test') -> Dict[str, Any]:
        """Perform statistical hypothesis tests for analytical validation."""
        if col1 not in data.columns or col2 not in data.columns:
            return {'error': 'Missing columns for hypothesis test'}

        if test_type == 't-test':
            stat, p_value = stats.ttest_ind(data[col1].dropna(), data[col2].dropna(), equal_var=False)
            return {'test': 't-test', 'statistic': float(stat), 'p_value': float(p_value)}
        elif test_type == 'chi2':
            contingency = pd.crosstab(data[col1], data[col2])
            stat, p_value, dof, expected = stats.chi2_contingency(contingency)
            return {
                'test': 'chi-square',
                'statistic': float(stat),
                'p_value': float(p_value),
                'dof': int(dof)
            }
        else:
            raise ValueError(f"Unsupported test type '{test_type}'")
