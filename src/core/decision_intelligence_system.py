from typing import Dict, List, Any
import uuid
from .data_loader import DataLoader
from .analyzer import RawDataAnalyzer
from .engines.validator import Validator
from .engines.root_cause import RootCauseEngine
from .engines.decision_engine import DecisionEngine
from .engines.confidence_engine import ConfidenceEngine
from .engines.limitation_engine import LimitationEngine
from .engines.consistency_engine import ConsistencyEngine
from .engines.audit_trail import AuditTrail
from .models.models import AnalysisResult

class DecisionIntelligenceSystem:
    """Orchestrator for end-to-end decision intelligence."""

    def __init__(self):
        self.data_loader = DataLoader()
        self.analyzer = RawDataAnalyzer()
        self.validator = Validator(self.data_loader, self.analyzer)
        self.root_cause = RootCauseEngine(self.data_loader, self.analyzer)
        self.decision_engine = DecisionEngine()
        self.confidence_engine = ConfidenceEngine()
        self.limitation_engine = LimitationEngine()
        self.consistency_engine = ConsistencyEngine()
        self.audit_trail = AuditTrail()

    def analyze_insight(self, insight_text: str, dataset_name: str, date_col: str = 'date', metric: str = 'sales') -> AnalysisResult:
        analysis_id = str(uuid.uuid4())
        result = AnalysisResult.create(analysis_id, insight_text)

        data = self.data_loader.get_dataframe(dataset_name)
        if data is None:
            result.validation = {'status': 'error', 'explanation': 'dataset not found'}
            return result

        self.audit_trail.log_operation('data_loaded', {'dataset': dataset_name, 'rows': len(data)}, analysis_id)

        result.metrics = {
            'summary': self.analyzer.statistical_summary(data),
            'trend': self.analyzer.trend_analysis(data, date_col, metric),
            'pct_change': self.analyzer.percentage_change(data, date_col, metric).tolist()
        }

        validation_result = self.validator.validate_insight(insight_text, dataset_name, date_col)
        result.validation = validation_result.__dict__

        root_cause_result = self.root_cause.find_root_causes(dataset_name, metric, [c for c in data.columns if c not in [date_col, metric]])
        result.root_cause = root_cause_result

        decision_actions = self.decision_engine.generate_decisions(validation_result, root_cause_result, result.metrics['trend'], len(data[data[metric].isnull()]), len(data))
        result.decision = {'actions': [a.__dict__ for a in decision_actions], 'summary': self.decision_engine.get_decision_summary(decision_actions)}

        result.confidence = self.confidence_engine.score_confidence(data, metric, validation_result, root_cause_result)

        limitations = self.limitation_engine.detect_limitations(data, metric, date_col)
        result.limitations = [l['description'] for l in limitations]

        result.consistency_checks = self.consistency_engine.check_consistency(data, validation_result, root_cause_result, result.metrics['trend'])

        result.audit_trail = self.audit_trail.get_trail(analysis_id)
        self.audit_trail.log_operation('analysis_completed', {'analysis_id': analysis_id})

        return result
