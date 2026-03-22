import pandas as pd
from core.data_loader import DataLoader


def test_load_csv_and_quality_metrics(tmp_path):
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'], 'sales': [100, 200]})
    file_path = tmp_path / 'test.csv'
    df.to_csv(file_path, index=False)

    loader = DataLoader()
    loaded = loader.load_csv(str(file_path), name='test', parse_dates=['date'])

    assert 'test' in loader.list_datasets()
    assert loaded.shape == (2, 2)

    quality = loader.get_quality_metrics('test')
    assert quality['rows'] == 2
    assert quality['duplicate_rows'] == 0


def test_clean_data_drops_all_na(tmp_path):
    df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'], 'sales': [None, None]})
    file_path = tmp_path / 'test.csv'
    df.to_csv(file_path, index=False)

    loader = DataLoader()
    loader.load_csv(str(file_path), name='test')
    cleaned = loader.clean_data('test', dropna_threshold=1.0)

    assert cleaned.empty
