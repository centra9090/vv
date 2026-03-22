import pandas as pd
from core.engines.limitation_engine import LimitationEngine
from core.engines.consistency_engine import ConsistencyEngine
from core.engines.decision_engine import DecisionEngine, Action, ActionType, Priority
from core.data_loader import DataLoader
from core.analyzer import RawDataAnalyzer
from core.engines.validator import Validator


def test_limitation_engine_small_dataset():
    df = pd.DataFrame({'date': ['2024-01-01'], 'sales': [100]})
    engine = LimitationEngine()
    limitations = engine.detect_limitations(df, 'sales', 'date')
    assert any(item['type'] == 'small_sample_size' for item in limitations)


def test_consistency_engine_alignment():
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'], 'sales': [100, 110]})
    loader = DataLoader(); loader.dataframes['test'] = df
    analyzer = RawDataAnalyzer()
    validator = Validator(loader, analyzer)
    validation = validator.validate_insight('sales increased 10%', 'test', 'date')
    root_cause_result = {'primary_root_cause': {'change': 10, 'contribution_pct': 60, 'dimension': 'date', 'group': '2024-01-02'}}
    trend = analyzer.trend_analysis(df, 'date', 'sales')

    engine = ConsistencyEngine()
    checks = engine.check_consistency(df, validation, root_cause_result, trend)
    assert isinstance(checks, list)


def test_decision_engine_actions():
    engine = DecisionEngine()
    class DummyVal: is_valid=False; error_margin=30; confidence=0.4
    validation = DummyVal()
    root_cause = {'primary_root_cause': {'change': -10, 'contribution_pct': 40, 'dimension': 'region', 'group': 'A'}}
    trend = {'slope': -1.0}
    actions = engine.generate_decisions(validation, root_cause, trend, anomaly_count=3, total_records=20)
    assert len(actions) >= 1
    assert any(a.priority == Priority.HIGH or a.priority == Priority.MEDIUM for a in actions)
