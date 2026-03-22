import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any

class DataLoader:
    """Flexible data loader for raw data analysis."""

    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = {}

    def load_csv(self,
                 file_path: str,
                 name: str,
                 dtype: Optional[Dict[str, Any]] = None,
                 parse_dates: Optional[List[str]] = None,
                 usecols: Optional[List[str]] = None,
                 nrows: Optional[int] = None,
                 chunksize: Optional[int] = None,
                 na_values: Optional[List[str]] = None,
                 schema: Optional[Dict[str, type]] = None) -> pd.DataFrame:
        """Load CSV file with optional schema and data quality checks."""
        read_opts: Dict[str, Any] = {
            'filepath_or_buffer': file_path,
            'dtype': dtype,
            'parse_dates': parse_dates,
            'usecols': usecols,
            'nrows': nrows,
            'na_values': na_values,
            'keep_default_na': True,
            'low_memory': False
        }

        if chunksize:
            chunks = pd.read_csv(**read_opts, chunksize=chunksize)
            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_csv(**read_opts)

        if schema is not None:
            df = self._apply_schema(df, schema)

        self.dataframes[name] = df
        return df

    def load_excel(self,
                   file_path: str,
                   name: str,
                   sheet_name: str = 0,
                   dtype: Optional[Dict[str, Any]] = None,
                   parse_dates: Optional[List[str]] = None,
                   usecols: Optional[List[str]] = None,
                   schema: Optional[Dict[str, type]] = None) -> pd.DataFrame:
        """Load Excel file with optional schema and validation."""
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=dtype, parse_dates=parse_dates, usecols=usecols)

        if schema is not None:
            df = self._apply_schema(df, schema)

        self.dataframes[name] = df
        return df

    def get_dataframe(self, name: str) -> Optional[pd.DataFrame]:
        """Retrieve loaded dataframe by name."""
        return self.dataframes.get(name)

    def list_datasets(self) -> List[str]:
        """List all loaded dataset names."""
        return list(self.dataframes.keys())

    def _apply_schema(self, df: pd.DataFrame, schema: Dict[str, type]) -> pd.DataFrame:
        """Validate column existence and cast types according to schema."""
        missing_cols = [col for col in schema if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required schema columns: {missing_cols}")

        for col, expected_type in schema.items():
            if expected_type is pd.Timestamp or expected_type == 'datetime':
                df[col] = pd.to_datetime(df[col], errors='coerce')
            else:
                try:
                    df[col] = df[col].astype(expected_type)
                except Exception:
                    df[col] = df[col].infer_objects()

        return df

    def clean_data(self, name: str, dropna_threshold: float = 0.95, remove_duplicates: bool = True) -> pd.DataFrame:
        """Basic cleaning routine with na/duplicate handling."""
        df = self.get_dataframe(name)
        if df is None:
            raise ValueError(f"Dataset '{name}' not loaded")

        # Drop rows with too many missing values
        df = df.dropna(thresh=int(df.shape[1] * dropna_threshold))

        if remove_duplicates:
            df = df.drop_duplicates()

        self.dataframes[name] = df
        return df

    def get_quality_metrics(self, name: str) -> Dict[str, Any]:
        """Return quick data quality metrics."""
        df = self.get_dataframe(name)
        if df is None:
            raise ValueError(f"Dataset '{name}' not loaded")

        n = len(df)
        missing = df.isnull().sum().to_dict()
        duplicates = int(df.duplicated().sum())

        return {
            'rows': n,
            'columns': df.shape[1],
            'missing_values': missing,
            'duplicate_rows': duplicates,
            'percent_duplicates': (duplicates / n) * 100 if n > 0 else 0
        }