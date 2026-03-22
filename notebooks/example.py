# Example: AI Decision Support System
# This script demonstrates both raw data analysis and multi-LLM integration

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.data_loader import DataLoader
from src.analyzer import RawDataAnalyzer
from src.llm_integrator import LLMIntegrator, OpenAIProvider

def main():
    print("🧠 AI Decision Support System Demo")
    print("=" * 50)

    # 1. Raw Data Analysis
    print("\n1. Raw Data Analysis (No AI Required)")
    loader = DataLoader()
    analyzer = RawDataAnalyzer()

    # Simulate loading data (replace with actual file)
    import pandas as pd
    import numpy as np

    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    sales = np.random.normal(10000, 2000, 100) + np.linspace(0, -500, 100)  # Declining trend
    df = pd.DataFrame({'date': dates, 'sales': sales})
    loader.dataframes['sales'] = df

    print(f"Loaded dataset with shape: {df.shape}")
    summary = analyzer.statistical_summary(df)
    print(f"Sales mean: ${summary['numeric_summary']['sales']['mean']:.2f}")

    # Detect anomalies
    anomalies = analyzer.detect_anomalies(df, 'sales')
    anomaly_count = anomalies['is_anomaly'].sum()
    print(f"Detected {anomaly_count} anomalies")

    # Trend analysis
    trend = analyzer.trend_analysis(df, 'date', 'sales')
    print(f"Trend: {trend['trend_direction']} (slope: {trend['slope']:.2f})")

    # 2. Multi-LLM Integration (if API keys available)
    print("\n2. Multi-LLM Integration")
    integrator = LLMIntegrator()

    try:
        integrator.add_provider('openai', OpenAIProvider())
        data_summary = f"Sales data: {len(df)} records, mean ${summary['numeric_summary']['sales']['mean']:.2f}, trend {trend['trend_direction']}"

        insights = integrator.generate_insight_multi(
            "Summarize the key insights from this sales data",
            data_summary,
            providers=['openai']
        )

        print("AI Insights:")
        for provider, insight in insights.items():
            print(f"- {provider}: {insight[:100]}...")

    except Exception as e:
        print(f"LLM integration skipped: {e}")
        print("To enable AI features, set API keys and install required packages")

    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()