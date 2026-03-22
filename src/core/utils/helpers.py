import pandas as pd
import numpy as np

def detect_outliers_zscore(data: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Detect outliers using z-score method."""
    if len(data) <= 1:
        return pd.Series([], dtype=bool)
    
    mean_val = data.mean()
    std_val = data.std()
    
    if std_val <= 1e-6:  # Near-zero std guard
        return pd.Series([False] * len(data), index=data.index)
    
    z_scores = np.abs((data - mean_val) / std_val)
    return z_scores > threshold

def detect_outliers_iqr(data: pd.Series, multiplier: float = 3.0) -> pd.Series:
    """Detect outliers using IQR method."""
    if len(data) <= 1:
        return pd.Series([], dtype=bool)
    
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    
    if iqr <= 1e-6:  # Near-zero IQR guard
        return pd.Series([False] * len(data), index=data.index)
    
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    return (data < lower_bound) | (data > upper_bound)