from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime, timedelta

class LimitationEngine:
    """Engine for detecting limitations and potential issues in analysis."""

    def __init__(self):
        pass

    def detect_limitations(self, data: pd.DataFrame, metric: str,
                          date_col: str = 'date') -> List[Dict[str, Any]]:
        """Detect various limitations in the dataset and analysis."""
        limitations = []

        # Check time range
        time_limitations = self._check_time_range(data, date_col)
        limitations.extend(time_limitations)

        # Check data quality
        quality_limitations = self._check_data_quality(data, metric)
        limitations.extend(quality_limitations)

        # Check dimensional coverage
        dimensional_limitations = self._check_dimensional_coverage(data)
        limitations.extend(dimensional_limitations)

        # Check sample representativeness
        representativeness_limitations = self._check_sample_representativeness(data)
        limitations.extend(representativeness_limitations)

        return limitations

    def _check_time_range(self, data: pd.DataFrame, date_col: str) -> List[Dict[str, Any]]:
        """Check if time range is sufficient for reliable analysis."""
        limitations = []

        if date_col not in data.columns:
            limitations.append({
                'type': 'missing_time_dimension',
                'severity': 'high',
                'description': 'No time dimension available for trend analysis',
                'impact': 'Cannot analyze trends or changes over time'
            })
            return limitations

        try:
            dates = pd.to_datetime(data[date_col])
            date_range = dates.max() - dates.min()

            # Check minimum time range
            if date_range < timedelta(days=30):
                limitations.append({
                    'type': 'insufficient_time_range',
                    'severity': 'high',
                    'description': f'Time range of {date_range.days} days is too short',
                    'impact': 'Limited ability to detect meaningful trends or patterns'
                })
            elif date_range < timedelta(days=90):
                limitations.append({
                    'type': 'limited_time_range',
                    'severity': 'medium',
                    'description': f'Time range of {date_range.days} days may limit analysis depth',
                    'impact': 'Some seasonal patterns may not be detectable'
                })

            # Check data frequency
            unique_dates = dates.nunique()
            expected_records = date_range.days + 1
            coverage = unique_dates / expected_records

            if coverage < 0.7:
                limitations.append({
                    'type': 'sparse_time_coverage',
                    'severity': 'medium',
                    'description': f'Only {coverage:.1%} of expected time periods have data',
                    'impact': 'Potential gaps in trend analysis'
                })

        except Exception as e:
            limitations.append({
                'type': 'time_parsing_error',
                'severity': 'high',
                'description': f'Could not parse time data: {str(e)}',
                'impact': 'Time-based analysis not possible'
            })

        return limitations

    def _check_data_quality(self, data: pd.DataFrame, metric: str) -> List[Dict[str, Any]]:
        """Check data quality issues."""
        limitations = []

        if metric not in data.columns:
            limitations.append({
                'type': 'missing_metric',
                'severity': 'critical',
                'description': f'Primary metric "{metric}" not found in data',
                'impact': 'Analysis cannot proceed'
            })
            return limitations

        # Check missing values
        missing_pct = data[metric].isnull().mean()
        if missing_pct > 0.1:
            limitations.append({
                'type': 'high_missing_data',
                'severity': 'high',
                'description': f'{missing_pct:.1%} of {metric} values are missing',
                'impact': 'Reduced reliability of analysis results'
            })

        # Check for constant values
        unique_vals = data[metric].nunique()
        if unique_vals == 1:
            limitations.append({
                'type': 'no_variance',
                'severity': 'high',
                'description': f'Metric {metric} has no variation (constant value)',
                'impact': 'Cannot analyze changes or trends'
            })

        # Check for extreme outliers
        if data[metric].dtype in ['int64', 'float64']:
            q1, q3 = data[metric].quantile([0.25, 0.75])
            iqr = q3 - q1
            outliers = data[(data[metric] < q1 - 3*iqr) | (data[metric] > q3 + 3*iqr)]
            if len(outliers) > len(data) * 0.05:
                limitations.append({
                    'type': 'extreme_outliers',
                    'severity': 'medium',
                    'description': f'{len(outliers)} extreme outliers detected ({len(outliers)/len(data):.1%})',
                    'impact': 'Outliers may skew analysis results'
                })

        return limitations

    def _check_dimensional_coverage(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Check if important dimensions are missing."""
        limitations = []

        # Common business dimensions
        expected_dimensions = ['product', 'region', 'channel', 'customer_segment']
        present_dimensions = [col for col in expected_dimensions if col in data.columns]

        missing_dimensions = [dim for dim in expected_dimensions if dim not in data.columns]
        if missing_dimensions:
            limitations.append({
                'type': 'missing_dimensions',
                'severity': 'medium',
                'description': f'Missing business dimensions: {", ".join(missing_dimensions)}',
                'impact': 'Limited ability to perform root cause analysis'
            })

        # Check dimension cardinality
        for dim in present_dimensions:
            unique_count = data[dim].nunique()
            if unique_count < 2:
                limitations.append({
                    'type': 'low_dimension_cardinality',
                    'severity': 'low',
                    'description': f'Dimension "{dim}" has only {unique_count} unique values',
                    'impact': 'Limited segmentation analysis'
                })

        return limitations

    def _check_sample_representativeness(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Check if sample is representative."""
        limitations = []

        n = len(data)
        if n < 30:
            limitations.append({
                'type': 'small_sample_size',
                'severity': 'high',
                'description': f'Sample size of {n} is very small',
                'impact': 'Statistical analysis may not be reliable'
            })
        elif n < 100:
            limitations.append({
                'type': 'limited_sample_size',
                'severity': 'medium',
                'description': f'Sample size of {n} may limit analysis depth',
                'impact': 'Some patterns may not be detectable'
            })

        return limitations