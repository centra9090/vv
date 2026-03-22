import pandas as pd
from core.decision_intelligence_system import DecisionIntelligenceSystem


def test_full_system_workflow():
    system = DecisionIntelligenceSystem()
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02', '2024-01-03'], 'sales': [100, 90, 85], 'region': ['A', 'A', 'B']})
    system.data_loader.dataframes['test'] = df

    result = system.analyze_insight('sales dropped 15%', 'test', 'date')
    assert result.validation['status'] in ['valid', 'invalid']
    assert 'decision' in result.__dict__
    assert 'confidence' in result.__dict__
