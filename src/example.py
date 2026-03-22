# Example: Decision Intelligence System Validator Demo

import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
import numpy as np

from core.data_loader import DataLoader
from core.analyzer import RawDataAnalyzer
from core.engines.validator import Validator

def main():
    print("🧠 Decision Intelligence System - Validator Demo")
    print("=" * 50)

    # Initialize components
    data_loader = DataLoader()
    analyzer = RawDataAnalyzer()
    validator = Validator(data_loader, analyzer)

    # Simulate dataset with declining sales
    print("\n1. Loading Dataset")
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    sales = np.random.normal(10000, 2000, 100) + np.linspace(0, -500, 100)  # Declining trend

    df = pd.DataFrame({'date': dates, 'sales': sales})
    data_loader.dataframes['sales_data'] = df

    print(f"Loaded dataset with {len(df)} records")
    print(f"Sales mean: ${df['sales'].mean():.2f}")
    # Calculate actual change for verification
    pct_changes = analyzer.percentage_change(df, 'date', 'sales')
    actual_change = pct_changes.iloc[-1]
    print(f"Actual recent change: {actual_change:.2f}%")
    # Test with incorrect insight
    print("\n2. Testing Insight Validation")
    insight = "sales dropped 20%"  # This is incorrect - actual change is different
    print(f"Testing insight: '{insight}'")

    result = validator.validate_insight(insight, 'sales_data')

    # Print structured result
    print("\n3. Validation Result:")
    print(f"Status: {result.status.upper()}")
    print(f"Metric: {result.metric}")
    print(f"Claimed Change: {result.claimed_value:+.1f}%")
    print(f"Actual Change: {result.actual_value:+.1f}%")
    print(f"Error Margin: {result.error_margin:.1f}%")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Explanation: {result.explanation}")

    # Test with correct insight
    print("\n4. Testing with Correct Insight")
    correct_insight = f"sales changed by {actual_change:+.1f}%"  # Use actual value
    print(f"Testing insight: '{correct_insight}'")

    correct_result = validator.validate_insight(correct_insight, 'sales_data')

    print("\nValidation Result:")
    print(f"Status: {correct_result.status.upper()}")
    print(f"Error Margin: {correct_result.error_margin:.1f}%")
    print(f"Confidence: {correct_result.confidence:.2f}")

    print("\n✅ Validator demo completed!")

if __name__ == "__main__":
    main()