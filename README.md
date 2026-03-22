# 🧠 AI Decision Support System for Data Analysis

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

## 📌 Overview

This project is a personal AI-assisted decision support system designed to bridge the gap between modern AI capabilities and real-world data analysis workflows. By leveraging advanced AI tools, it accelerates data analysis processes while ensuring accuracy and reliability.

**Key Principles for Flexibility:**
- **Multi-LLM Support**: Not dependent on a single Large Language Model; supports integration with multiple providers (OpenAI, Anthropic, Google, local models) for diverse insights and redundancy.
- **Raw Data Analysis**: Core functionality built on traditional statistical and machine learning methods, allowing analysis of raw data without mandatory AI dependency.

Instead of only generating insights, this tool focuses on:

- **Validating AI-generated insights** against real data
- **Finding root causes automatically** through intelligent analysis
- **Connecting multiple data domains** for comprehensive insights
- **Providing actionable recommendations** with confidence scores

The goal is to demonstrate advanced analytical thinking and system design skills beyond traditional dashboards, making data analysis faster and more efficient with cutting-edge AI assistance.

## 🎯 Objectives

- Build a system that does not blindly trust AI outputs
- Transform raw data into validated, explainable decisions
- Showcase end-to-end analytical thinking
- Serve as a portfolio project to increase value as a data analyst
- Accelerate workflows using AI-powered tools like GitHub Copilot

## 🚨 Problem Statement

Most current tools:

- Generate insights but do not validate them
- Provide dashboards but lack decision guidance
- Fail to connect cross-domain data (sales, users, marketing)
- Require analysts to manually find root causes
- Are slow in processing large datasets without AI assistance

## 💡 Solution

This project introduces a flexible system that:

1. **Generates insights using AI** (e.g., via LLMs or automated scripts) - with support for multiple LLM providers
2. **Validates those insights using real data** with statistical methods (works independently of AI)
3. **Identifies root causes automatically** through anomaly detection (ML-based, no AI required)
4. **Connects multiple data domains** for holistic analysis
5. **Outputs actionable business recommendations** prioritized by impact

**Flexibility Features:**
- **Multi-LLM Integration**: Switch between OpenAI GPT, Anthropic Claude, Google Gemini, or local models like Ollama for insight generation.
- **Raw Data Core**: All analysis can run on pure statistical/ML methods without AI, ensuring reliability and cost-effectiveness.

## 🧩 Core Features

### 1. 🤖 Insight Generator (AI Layer)
- Generate insights from datasets using AI models
- Summarize trends, anomalies, and patterns
- **Multi-LLM Support**: Integrate with OpenAI, Anthropic, Google, or local LLMs for diverse perspectives
- **Raw Data Fallback**: Generate insights using statistical analysis when AI is unavailable
- **AI Acceleration**: Use GitHub Copilot to auto-generate analysis code snippets

### 2. ✅ AI Validator (Key Feature)
- Cross-check AI-generated insights with actual data
- Output:
  - Valid / Invalid status
  - Confidence score (0-100%)
- **Flexible Validation**: Can validate using statistical tests (t-tests, chi-square) without AI dependency
- **AI Integration**: Leverage AI for automated validation scripts when available

### 3. 🔍 Auto Root Cause Analysis
- Detect anomalies (e.g., drop in sales)
- Break down by dimensions: Product, Region, Time
- Identify main contributing factors using statistical models
- **AI Enhancement**: AI-assisted anomaly detection algorithms

### 4. 🔗 Cross-Domain Analysis
Connect multiple datasets:
- User Activity → Sales
- Marketing → Revenue

Example: *"Drop in sales is caused by reduced user traffic from marketing campaigns."*

- **AI Tools**: Use AI to suggest correlations and connections

### 5. 🎯 Decision Recommendation Engine
- Translate insights into prioritized actions
- Prioritize business decisions based on impact and feasibility
- **AI Acceleration**: AI-generated recommendation templates

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- Required libraries: pandas, numpy, scikit-learn, matplotlib, seaborn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/centra9090/vv.git
   cd vv
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

4. (Optional) Set up LLM API keys:
   ```bash
   export OPENAI_API_KEY="your-key"
   export ANTHROPIC_API_KEY="your-key"
   export GOOGLE_API_KEY="your-key"
   ```

### Project Structure

```
vv/
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Raw data loading utilities
│   ├── analyzer.py         # Statistical analysis without AI
│   └── llm_integrator.py   # Multi-LLM support
├── requirements.txt
├── README.md
└── notebooks/              # Jupyter notebooks for examples
```

### Usage

#### Raw Data Analysis (No AI Required)
```python
from src.data_loader import DataLoader
from src.analyzer import RawDataAnalyzer

# Load data
loader = DataLoader()
df = loader.load_csv('sales_data.csv', 'sales')

# Analyze
analyzer = RawDataAnalyzer()
summary = analyzer.statistical_summary(df)
anomalies = analyzer.detect_anomalies(df, 'revenue')
correlations = analyzer.correlation_analysis(df)
```

#### Multi-LLM Integration
```python
from src.llm_integrator import LLMIntegrator, OpenAIProvider, AnthropicProvider

# Set up providers
integrator = LLMIntegrator()
integrator.add_provider('openai', OpenAIProvider())
integrator.add_provider('anthropic', AnthropicProvider())

# Generate insights from multiple LLMs
insights = integrator.generate_insight_multi(
    "What are the key trends in this sales data?",
    "Sales data summary: average revenue $10k, trending down 5%..."
)

# Validate with consensus
validations = integrator.validate_insight_multi(
    "Sales are declining due to poor marketing",
    "Detailed sales and marketing data..."
)
consensus = integrator.get_consensus_validation(validations)
```

### Usage

1. **Data Preparation**: Load your datasets into the system.
2. **AI Insight Generation**: Run the insight generator to get initial hypotheses.
3. **Validation**: Use the validator to confirm insights with data.
4. **Root Cause Analysis**: Analyze anomalies and identify causes.
5. **Recommendations**: Get actionable business decisions.

Example workflow in Jupyter:
```python
from ai_validator import validate_insight
from root_cause_analyzer import analyze_anomaly

# Load data
data = pd.read_csv('your_data.csv')

# Generate and validate insight
insight = "Sales dropped by 20% in Q4"
is_valid, confidence = validate_insight(insight, data)
print(f"Insight valid: {is_valid}, Confidence: {confidence}%")

# Analyze root cause
causes = analyze_anomaly(data, 'sales', 'Q4')
print(causes)
```

## 🤖 AI Integration for Faster Workflows

To leverage advanced AI for data analysis:

- **GitHub Copilot**: Use in VS Code for auto-completing code, generating functions, and debugging.
- **AI-Powered Tools**: Integrate with OpenAI API or similar for natural language queries on data.
- **Automation**: Scripts that use AI to preprocess data, detect outliers, and generate reports.
- **Best Practices**:
  - Prompt AI tools with specific data contexts for better results.
  - Validate AI outputs manually for critical decisions.
  - Use AI to prototype analyses quickly before refining.

## 📊 Example Use Case

Imagine a retail company with sales, user, and marketing data:

1. AI detects a sales anomaly.
2. Validator confirms it's real (95% confidence).
3. Root cause: Marketing spend decreased in key regions.
4. Recommendation: Reallocate budget to high-performing channels.

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Use AI tools like Copilot to assist in coding and documentation.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Troubleshooting

- **Import Errors**: Ensure you're running from the project root and dependencies are installed (`pip install -r requirements.txt`)
- **LLM Integration**: Set API keys as environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY)
- **Data Loading**: Support for CSV, Excel files; ensure file paths are correct

## 📞 Contact

For questions or suggestions, open an issue on GitHub.

---

*Flexible data analysis: Raw power meets AI intelligence.*

---

6. 🗣️ Business Translator

- Convert technical analysis into human-readable explanations
- Target: non-technical stakeholders

---

🏗️ System Architecture

DATA SOURCES
   ↓
[Data Engine]
   - Load & process data
   - Aggregation & metrics
   ↓
[Insight Engine]
   - AI-generated insights
   ↓
[Validator Engine] 🔥
   - Verify insights against data
   ↓
[Root Cause Engine]
   - Identify drivers of change
   ↓
[Decision Engine]
   - Recommend actions
   ↓
[Translator Layer]
   - Human-readable output

---

🗂️ Project Structure

project/
│
├── data/
│   └── sample_data.csv
│
├── core/
│   ├── loader.py          # Load dataset
│   ├── analysis.py        # Core calculations
│   ├── validator.py       # Insight validation
│   └── root_cause.py      # Root cause logic
│
├── ai/
│   └── insight.py         # AI-generated insights
│
├── decision/
│   └── recommender.py     # Decision logic
│
├── app/
│   └── main.py            # Entry point / UI
│
└── README.md

---

📊 Example Workflow

1. Upload dataset (e.g., sales data)

2. AI generates insight:
   
   «"Sales dropped by 20%"»

3. Validator checks:
   
   «❌ Incorrect (actual drop: 8%)»

4. Root cause analysis:
   
   «Drop driven by Product A in Region X»

5. Final output:
   
   «Sales decline is localized. Focus on Product A performance instead of global strategy.»

---

⚙️ Tech Stack

Core Engine

- Python (initial development)
- Optional: Rust (for performance optimization)

Data Processing

- Pandas / Polars

AI Layer

- LLM API (for insight generation & explanation)

Interface

- Streamlit (for quick UI)

---

🚀 Development Roadmap

Phase 1 (MVP)

- Load data
- Basic analysis
- Simple AI insight

---

Phase 2 (Core Differentiator)

- Implement AI Validator

---

Phase 3

- Add Root Cause Analysis

---

Phase 4

- Cross-domain logic
- Decision recommendations

---

Phase 5 (Advanced)

- Context-aware AI
- Simulation engine

---

🧠 Key Differentiation

Unlike typical tools, this system focuses on:

- Truth over automation
- Validation over generation
- Decision over visualization

---

📌 Future Improvements

- Real-time data integration
- Local LLM support
- Advanced simulation models
- Multi-user support

---

🎯 Target Outcome

This project aims to demonstrate:

- Strong analytical thinking
- Ability to design systems (not just analysis)
- Understanding of AI limitations
- Focus on business impact

---

🧑‍💻 Author Notes

This is a personal project built to:

- Enhance data analyst capabilities
- Explore AI + analytics integration
- Showcase problem-solving approach

---

📜 License

For personal and educational use.
