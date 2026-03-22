import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns

class RawDataAnalyzer:
    """Analyzer for raw data using statistical and ML methods without AI dependency."""

    def __init__(self):
        self.scaler = StandardScaler()

    def detect_anomalies(self, data: pd.DataFrame, column: str, contamination: float = 0.1) -> pd.DataFrame:
        """Detect anomalies using Isolation Forest."""
        numeric_data = data.select_dtypes(include=[np.number])
        if column not in numeric_data.columns:
            raise ValueError(f"Column {column} not found or not numeric")

        # Fit isolation forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        scaled_data = self.scaler.fit_transform(numeric_data)
        anomalies = iso_forest.fit_predict(scaled_data)

        # Add anomaly column
        result = data.copy()
        result['anomaly_score'] = anomalies
        result['is_anomaly'] = anomalies == -1
        return result

    def statistical_summary(self, data: pd.DataFrame) -> Dict:
        """Generate statistical summary of the dataset."""
        summary = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'numeric_summary': data.describe().to_dict()
        }
        return summary

    def correlation_analysis(self, data: pd.DataFrame) -> pd.DataFrame:
        """Compute correlation matrix for numeric columns."""
        numeric_data = data.select_dtypes(include=[np.number])
        return numeric_data.corr()

    def hypothesis_test(self, data: pd.DataFrame, col1: str, col2: str,
                       test_type: str = 't-test') -> Dict:
        """Perform statistical hypothesis tests."""
        if test_type == 't-test':
            stat, p_value = stats.ttest_ind(data[col1], data[col2])
            return {'test': 't-test', 'statistic': stat, 'p_value': p_value}
        elif test_type == 'chi2':
            contingency = pd.crosstab(data[col1], data[col2])
            stat, p_value, dof, expected = stats.chi2_contingency(contingency)
            return {'test': 'chi-square', 'statistic': stat, 'p_value': p_value, 'dof': dof}
        else:
            raise ValueError("Unsupported test type")

    def trend_analysis(self, data: pd.DataFrame, date_col: str, value_col: str) -> Dict:
        """Analyze trends over time."""
        data[date_col] = pd.to_datetime(data[date_col])
        data = data.sort_values(date_col)

        # Simple linear trend
        x = np.arange(len(data))
        y = data[value_col].values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'p_value': p_value,
            'trend_direction': 'increasing' if slope > 0 else 'decreasing'
        }

    def plot_distribution(self, data: pd.DataFrame, column: str, save_path: Optional[str] = None):
        """Plot distribution of a column."""
        plt.figure(figsize=(10, 6))
        sns.histplot(data[column], kde=True)
        plt.title(f'Distribution of {column}')
        if save_path:
            plt.savefig(save_path)
        plt.show()

    def root_cause_candidates(self, data: pd.DataFrame, target_col: str,
                            group_cols: List[str]) -> pd.DataFrame:
        """Find potential root causes by grouping and analyzing variance."""
        results = []
        for col in group_cols:
            grouped = data.groupby(col)[target_col].agg(['mean', 'std', 'count'])
            grouped['variance'] = grouped['std'] ** 2
            grouped['impact_score'] = grouped['mean'] * grouped['count']  # Simple impact metric
            results.append(grouped.reset_index().assign(group_by=col))

        return pd.concat(results, ignore_index=True)