from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

from ..data_loader import DataLoader
from ..analyzer import RawDataAnalyzer

class RootCauseEngine:
    """Engine for identifying root causes of changes in metrics."""

    def __init__(self, data_loader: DataLoader, analyzer: RawDataAnalyzer):
        self.data_loader = data_loader
        self.analyzer = analyzer

    def analyze_contribution(self, data: pd.DataFrame, metric: str,
                           group_by: str, date_col: str = 'date',
                           periods: int = 1) -> Dict[str, Any]:
        """Analyze contribution of groups to overall metric change."""
        if group_by not in data.columns or metric not in data.columns:
            return {'error': f'Column {group_by} or {metric} not found'}

        # Sort by date
        data = data.sort_values(date_col).copy()

        # Get recent periods
        recent_period = data.tail(periods)
        previous_period = data.head(-periods).tail(periods) if len(data) > periods else data.head(len(recent_period))

        if previous_period.empty:
            return {'error': 'Not enough data for comparison'}

        # Calculate changes by group
        contributions = []
        total_change = 0

        for group_value in data[group_by].unique():
            recent_group = recent_period[recent_period[group_by] == group_value]
            prev_group = previous_period[previous_period[group_by] == group_value]

            if not recent_group.empty and not prev_group.empty:
                recent_avg = recent_group[metric].mean()
                prev_avg = prev_group[metric].mean()
                change = recent_avg - prev_avg
                total_change += change

                contributions.append({
                    'group': group_value,
                    'recent_avg': recent_avg,
                    'prev_avg': prev_avg,
                    'change': change,
                    'contribution_pct': 0  # Will calculate after
                })

        # Calculate percentage contributions
        if total_change != 0:
            for contrib in contributions:
                contrib['contribution_pct'] = (contrib['change'] / abs(total_change)) * 100

        # Sort by absolute contribution
        contributions.sort(key=lambda x: abs(x['change']), reverse=True)

        return {
            'total_change': total_change,
            'contributions': contributions,
            'top_contributor': contributions[0] if contributions else None
        }

    def find_root_causes(self, dataset_name: str, metric: str,
                        dimensions: List[str], date_col: str = 'date') -> Dict[str, Any]:
        """Find root causes across multiple dimensions."""
        data = self.data_loader.get_dataframe(dataset_name)
        if data is None:
            return {'error': f'Dataset {dataset_name} not found'}

        results = {}
        for dimension in dimensions:
            analysis = self.analyze_contribution(data, metric, dimension, date_col)
            if 'error' not in analysis:
                results[dimension] = analysis

        # Identify primary root cause
        primary_cause = None
        max_contribution = 0

        for dim, analysis in results.items():
            if analysis['contributions']:
                top = analysis['contributions'][0]
                if abs(top['contribution_pct']) > max_contribution:
                    max_contribution = abs(top['contribution_pct'])
                    primary_cause = {
                        'dimension': dim,
                        'group': top['group'],
                        'contribution_pct': top['contribution_pct'],
                        'change': top['change']
                    }

        return {
            'metric': metric,
            'analyses': results,
            'primary_root_cause': primary_cause,
            'summary': self._generate_summary(primary_cause) if primary_cause else "No significant root cause identified"
        }

    def _generate_summary(self, primary_cause: Dict[str, Any]) -> str:
        """Generate human-readable summary of root cause."""
        dim = primary_cause['dimension']
        group = primary_cause['group']
        pct = primary_cause['contribution_pct']
        change = primary_cause['change']

        direction = "increase" if change > 0 else "decrease"
        return f"{group} in {dim} is responsible for {abs(pct):.1f}% of the total {direction}"