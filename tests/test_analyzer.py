import pandas as pd
from core.analyzer import RawDataAnalyzer


def test_statistical_summary_and_trend_analysis():
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02', '2024-01-03'], 'sales': [100, 150, 120]})
    analyzer = RawDataAnalyzer()

    summary = analyzer.statistical_summary(df)
    assert summary['shape'] == (3, 2)
    assert summary['duplicate_rows'] == 0

    trend = analyzer.trend_analysis(df, 'date', 'sales')
    assert trend['trend_direction'] in ['increasing', 'decreasing', 'stable']

    pct = analyzer.percentage_change(df, 'date', 'sales')
    assert pd.isna(pct.iloc[0])
    assert pct.iloc[1] == 50.0
    assert round(pct.iloc[2], 6) == -20.0


def test_validate_metric_range():
    df = pd.DataFrame({'sales': [100, 150, 120]})
    analyzer = RawDataAnalyzer()

    result = analyzer.validate_metric_range(df, 'sales', 90, 200)
    assert result['valid'] is True
    assert result['percentage_valid'] == 100.0
