from typing import Optional, Dict, Any, List
import os
from abc import ABC, abstractmethod

# Conditional imports for different LLM providers
try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_insight(self, prompt: str, data_summary: str) -> str:
        """Generate insight from data summary."""
        pass

    @abstractmethod
    def validate_insight(self, insight: str, data_summary: str) -> Dict[str, Any]:
        """Validate an insight against data."""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        if openai is None:
            raise ImportError("OpenAI package not installed")
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_insight(self, prompt: str, data_summary: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a data analyst generating insights from data."},
                {"role": "user", "content": f"Data Summary: {data_summary}\n\nPrompt: {prompt}"}
            ]
        )
        return response.choices[0].message.content

    def validate_insight(self, insight: str, data_summary: str) -> Dict[str, Any]:
        prompt = f"Validate this insight against the data: '{insight}'\nData: {data_summary}\nReturn confidence score (0-100) and validity (True/False)."
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        # Parse response (simplified)
        content = response.choices[0].message.content.lower()
        is_valid = "true" in content
        confidence = 50  # Default, could parse from response
        return {"valid": is_valid, "confidence": confidence}

class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        if anthropic is None:
            raise ImportError("Anthropic package not installed")
        self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def generate_insight(self, prompt: str, data_summary: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"Data Summary: {data_summary}\n\nPrompt: {prompt}"}
            ]
        )
        return response.content[0].text

    def validate_insight(self, insight: str, data_summary: str) -> Dict[str, Any]:
        prompt = f"Validate this insight: '{insight}'\nData: {data_summary}\nReturn validity and confidence."
        response = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text.lower()
        is_valid = "valid" in content or "true" in content
        confidence = 50
        return {"valid": is_valid, "confidence": confidence}

class GoogleProvider(LLMProvider):
    """Google Gemini provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        if genai is None:
            raise ImportError("Google Generative AI package not installed")
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model)

    def generate_insight(self, prompt: str, data_summary: str) -> str:
        response = self.model.generate_content(f"Data Summary: {data_summary}\n\nPrompt: {prompt}")
        return response.text

    def validate_insight(self, insight: str, data_summary: str) -> Dict[str, Any]:
        prompt = f"Validate: '{insight}'\nData: {data_summary}"
        response = self.model.generate_content(prompt)
        content = response.text.lower()
        is_valid = "valid" in content
        confidence = 50
        return {"valid": is_valid, "confidence": confidence}

class LLMIntegrator:
    """Multi-LLM integrator for flexible AI support."""

    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {}

    def add_provider(self, name: str, provider: LLMProvider):
        """Add an LLM provider."""
        self.providers[name] = provider

    def generate_insight_multi(self, prompt: str, data_summary: str,
                              providers: Optional[List[str]] = None) -> Dict[str, str]:
        """Generate insights from multiple providers."""
        if providers is None:
            providers = list(self.providers.keys())

        results = {}
        for name in providers:
            if name in self.providers:
                try:
                    results[name] = self.providers[name].generate_insight(prompt, data_summary)
                except Exception as e:
                    results[name] = f"Error: {str(e)}"
        return results

    def validate_insight_multi(self, insight: str, data_summary: str,
                              providers: Optional[List[str]] = None) -> Dict[str, Dict]:
        """Validate insight using multiple providers."""
        if providers is None:
            providers = list(self.providers.keys())

        results = {}
        for name in providers:
            if name in self.providers:
                try:
                    results[name] = self.providers[name].validate_insight(insight, data_summary)
                except Exception as e:
                    results[name] = {"error": str(e)}
        return results

    def get_consensus_validation(self, validations: Dict[str, Dict]) -> Dict[str, Any]:
        """Get consensus from multiple validations."""
        valid_count = sum(1 for v in validations.values() if v.get("valid", False))
        total = len(validations)
        confidence_avg = sum(v.get("confidence", 0) for v in validations.values()) / total if total > 0 else 0

        return {
            "consensus_valid": valid_count > total / 2,
            "agreement_ratio": valid_count / total if total > 0 else 0,
            "average_confidence": confidence_avg
        }