import pandas as pd
from core.data_loader import DataLoader
from core.analyzer import RawDataAnalyzer
from core.engines.validator import Validator


def test_validator_valid_and_invalid():
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02', '2024-01-03'], 'sales': [100, 90, 85]})
    loader = DataLoader()
    loader.dataframes['test'] = df
    validator = Validator(loader, RawDataAnalyzer())

    invalid_result = validator.validate_insight('sales dropped 20%', 'test', 'date')
    assert invalid_result.status == 'invalid'

    # actual latest change is approximately -5.56% (from 90 to 85); tolerance 5% makes -5.6 plausible invalid.
    valid_result = validator.validate_insight('sales dropped 5.6%', 'test', 'date')
    assert valid_result.status == 'valid'
    assert 0.0 <= valid_result.confidence <= 1.0
