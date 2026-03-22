import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class DataLoader:
    """Flexible data loader for raw data analysis."""

    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = {}

    def load_csv(self, file_path: str, name: str) -> pd.DataFrame:
        """Load CSV file into memory."""
        df = pd.read_csv(file_path)
        self.dataframes[name] = df
        return df

    def load_excel(self, file_path: str, name: str, sheet_name: str = 0) -> pd.DataFrame:
        """Load Excel file into memory."""
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        self.dataframes[name] = df
        return df

    def get_dataframe(self, name: str) -> Optional[pd.DataFrame]:
        """Retrieve loaded dataframe by name."""
        return self.dataframes.get(name)

    def list_datasets(self) -> List[str]:
        """List all loaded dataset names."""
        return list(self.dataframes.keys())