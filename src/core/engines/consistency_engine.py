from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

class ConsistencyEngine:
    """Engine for checking consistency across analysis results."""

    def __init__(self):
        pass

    def check_consistency(self, data: pd.DataFrame, validation_result: Any,
                         root_cause_result: Dict[str, Any], trend_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform consistency checks across all analysis components."""
        checks = []

        # Check validation vs root cause alignment
        validation_checks = self._check_validation_root_cause_alignment(validation_result, root_cause_result)
        checks.extend(validation_checks)

        # Check trend vs validation alignment
        trend_checks = self._check_trend_validation_alignment(trend_result, validation_result)
        checks.extend(trend_checks)

        # Check for contradictory signals
        contradiction_checks = self._check_contradictory_signals(data, validation_result, root_cause_result)
        checks.extend(contradiction_checks)

        # Check data consistency
        data_checks = self._check_data_consistency(data)
        checks.extend(data_checks)

        return checks

    def _check_validation_root_cause_alignment(self, validation_result: Any,
                                             root_cause_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if validation and root cause results align."""
        checks = []

        if not hasattr(validation_result, 'claimed_value') or not hasattr(validation_result, 'actual_value'):
            return checks

        claimed_direction = 'increase' if validation_result.claimed_value > 0 else 'decrease'
        actual_direction = 'increase' if validation_result.actual_value > 0 else 'decrease'

        primary_cause = root_cause_result.get('primary_root_cause')
        if primary_cause:
            root_cause_change = primary_cause.get('change', 0)
            root_cause_direction = 'increase' if root_cause_change > 0 else 'decrease'

            # Check if all three align
            if claimed_direction == actual_direction == root_cause_direction:
                checks.append({
                    'check_type': 'alignment',
                    'component': 'validation_root_cause_trend',
                    'status': 'consistent',
                    'severity': 'info',
                    'message': 'Validation, actual data, and root cause all show consistent direction'
                })
            else:
                inconsistencies = []
                if claimed_direction != actual_direction:
                    inconsistencies.append('validation vs actual data')
                if actual_direction != root_cause_direction:
                    inconsistencies.append('actual data vs root cause')

                checks.append({
                    'check_type': 'alignment',
                    'component': 'validation_root_cause_trend',
                    'status': 'inconsistent',
                    'severity': 'warning',
                    'message': f'Inconsistencies found in: {", ".join(inconsistencies)}'
                })

        return checks

    def _check_trend_validation_alignment(self, trend_result: Dict[str, Any],
                                        validation_result: Any) -> List[Dict[str, Any]]:
        """Check if trend analysis aligns with validation."""
        checks = []

        if 'slope' not in trend_result or not hasattr(validation_result, 'actual_value'):
            return checks

        trend_slope = trend_result['slope']
        validation_change = validation_result.actual_value

        # Determine directions
        trend_direction = 'increasing' if trend_slope > 0.01 else 'decreasing' if trend_slope < -0.01 else 'stable'
        validation_direction = 'increasing' if validation_change > 0 else 'decreasing' if validation_change < 0 else 'stable'

        if trend_direction == validation_direction:
            checks.append({
                'check_type': 'trend_alignment',
                'component': 'trend_validation',
                'status': 'consistent',
                'severity': 'info',
                'message': f'Trend ({trend_direction}) aligns with validation result ({validation_direction})'
            })
        elif trend_direction == 'stable' or validation_direction == 'stable':
            checks.append({
                'check_type': 'trend_alignment',
                'component': 'trend_validation',
                'status': 'partial',
                'severity': 'info',
                'message': f'Trend shows {trend_direction} while validation shows {validation_direction}'
            })
        else:
            checks.append({
                'check_type': 'trend_alignment',
                'component': 'trend_validation',
                'status': 'inconsistent',
                'severity': 'warning',
                'message': f'Trend direction ({trend_direction}) contradicts validation ({validation_direction})'
            })

        return checks

    def _check_contradictory_signals(self, data: pd.DataFrame, validation_result: Any,
                                   root_cause_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for contradictory signals in the analysis."""
        checks = []

        # Check for high error margin with strong root cause
        if hasattr(validation_result, 'error_margin') and validation_result.error_margin > 20:
            primary_cause = root_cause_result.get('primary_root_cause')
            if primary_cause and abs(primary_cause.get('contribution_pct', 0)) > 50:
                checks.append({
                    'check_type': 'signal_contradiction',
                    'component': 'error_margin_vs_root_cause',
                    'status': 'warning',
                    'severity': 'warning',
                    'message': f'High validation error ({validation_result.error_margin:.1f}%) with strong root cause signal may indicate data issues'
                })

        # Check for anomalies in data that might affect reliability
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col in ['date', 'index']:
                continue

            # Simple outlier detection
            if len(data) > 10:
                mean_val = data[col].mean()
                std_val = data[col].std()
                if std_val > 0:
                    outliers = data[abs(data[col] - mean_val) > 3 * std_val]
                    if len(outliers) > len(data) * 0.1:  # More than 10% outliers
                        checks.append({
                            'check_type': 'data_quality',
                            'component': f'{col}_outliers',
                            'status': 'warning',
                            'severity': 'warning',
                            'message': f'Column {col} has {len(outliers)} outliers ({len(outliers)/len(data):.1%} of data)'
                        })

        return checks

    def _check_data_consistency(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Check for data consistency issues."""
        checks = []

        # Check for missing values
        missing_summary = data.isnull().sum()
        total_missing = missing_summary.sum()

        if total_missing > 0:
            missing_pct = total_missing / (len(data) * len(data.columns)) * 100
            if missing_pct > 5:
                checks.append({
                    'check_type': 'data_completeness',
                    'component': 'missing_values',
                    'status': 'warning',
                    'severity': 'warning',
                    'message': f'Dataset has {total_missing} missing values ({missing_pct:.1f}% of total data)'
                })

        # Check for duplicate rows
        duplicates = data.duplicated().sum()
        if duplicates > 0:
            dup_pct = duplicates / len(data) * 100
            checks.append({
                'check_type': 'data_integrity',
                'component': 'duplicate_rows',
                'status': 'warning',
                'severity': 'info',
                'message': f'Found {duplicates} duplicate rows ({dup_pct:.1f}% of data)'
            })

        # Check date column consistency if exists
        date_cols = [col for col in data.columns if 'date' in col.lower()]
        for date_col in date_cols:
            try:
                pd.to_datetime(data[date_col])
            except:
                checks.append({
                    'check_type': 'data_format',
                    'component': f'{date_col}_format',
                    'status': 'error',
                    'severity': 'error',
                    'message': f'Column {date_col} contains invalid date formats'
                })

        return checks