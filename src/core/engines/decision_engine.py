from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ActionType(Enum):
    INVESTIGATE = "investigate"
    MONITOR = "monitor"
    ACT = "act"
    REVIEW = "review"

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Action:
    """Recommended action based on analysis."""
    action_type: ActionType
    priority: Priority
    description: str
    rationale: str
    expected_impact: str

class DecisionEngine:
    """Engine for generating actionable recommendations based on analysis results."""

    def __init__(self):
        pass

    def generate_decisions(self, validation_result: Any,
                          root_cause_result: Dict[str, Any],
                          trend_result: Dict[str, Any],
                          anomaly_count: int,
                          total_records: int) -> List[Action]:
        """Generate list of recommended actions based on analysis."""
        actions = []

        # Analyze validation results
        validation_actions = self._analyze_validation(validation_result)
        actions.extend(validation_actions)

        # Analyze root cause results
        root_cause_actions = self._analyze_root_cause(root_cause_result)
        actions.extend(root_cause_actions)

        # Analyze trends
        trend_actions = self._analyze_trends(trend_result, anomaly_count, total_records)
        actions.extend(trend_actions)

        # Sort by priority
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        actions.sort(key=lambda x: priority_order[x.priority])

        return actions

    def _analyze_validation(self, validation_result: Any) -> List[Action]:
        """Generate actions based on validation results."""
        actions = []

        is_valid = None
        if hasattr(validation_result, 'is_valid'):
            is_valid = validation_result.is_valid
        elif hasattr(validation_result, 'status'):
            is_valid = validation_result.status == 'valid'

        if is_valid is None:
            return actions

        if not is_valid:
            actions.append(Action(
                action_type=ActionType.INVESTIGATE,
                priority=Priority.HIGH,
                description="Investigate the source of the invalid insight claim",
                rationale=f"Validation failed with {getattr(validation_result, 'error_margin', 0):.1f}% error margin",
                expected_impact="Prevent future incorrect claims and improve data accuracy"
            ))

        confidence = getattr(validation_result, 'confidence', 0.5)
        if confidence < 0.6:
            actions.append(Action(
                action_type=ActionType.REVIEW,
                priority=Priority.MEDIUM,
                description="Review data collection and validation processes",
                rationale=f"Low confidence score ({confidence:.2f}) indicates potential data quality issues",
                expected_impact="Improve reliability of future validations"
            ))

        return actions

    def _analyze_root_cause(self, root_cause_result: Dict[str, Any]) -> List[Action]:
        """Generate actions based on root cause analysis."""
        actions = []

        primary_cause = root_cause_result.get('primary_root_cause')
        if primary_cause:
            contribution = abs(primary_cause.get('contribution_pct', 0))
            dimension = primary_cause.get('dimension')
            group = primary_cause.get('group')

            if contribution > 30:
                # Significant root cause found
                actions.append(Action(
                    action_type=ActionType.ACT,
                    priority=Priority.HIGH,
                    description=f"Address {group} in {dimension} category",
                    rationale=f"Responsible for {contribution:.1f}% of the observed change",
                    expected_impact="Directly impact the key driver of the metric change"
                ))
            elif contribution > 15:
                # Moderate root cause
                actions.append(Action(
                    action_type=ActionType.MONITOR,
                    priority=Priority.MEDIUM,
                    description=f"Monitor {group} in {dimension} closely",
                    rationale=f"Contributes {contribution:.1f}% to the change",
                    expected_impact="Track potential emerging issues"
                ))

        return actions

    def _analyze_trends(self, trend_result: Dict[str, Any],
                       anomaly_count: int, total_records: int) -> List[Action]:
        """Generate actions based on trend analysis."""
        actions = []

        # Check for anomalies
        anomaly_rate = anomaly_count / total_records if total_records > 0 else 0
        if anomaly_rate > 0.1:  # More than 10% anomalies
            actions.append(Action(
                action_type=ActionType.INVESTIGATE,
                priority=Priority.HIGH,
                description="Investigate anomalous data points",
                rationale=f"Found {anomaly_count} anomalies ({anomaly_rate:.1%} of data)",
                expected_impact="Identify and address data quality or process issues"
            ))

        # Check trend direction if available
        if 'slope' in trend_result:
            slope = trend_result['slope']
            if slope < -0.1:  # Significant downward trend
                actions.append(Action(
                    action_type=ActionType.MONITOR,
                    priority=Priority.MEDIUM,
                    description="Monitor downward trend closely",
                    rationale="Significant declining trend detected",
                    expected_impact="Enable early intervention if trend continues"
                ))

        return actions

    def get_decision_summary(self, actions: List[Action]) -> Dict[str, Any]:
        """Generate summary of recommended actions."""
        if not actions:
            return {"summary": "No specific actions recommended", "total_actions": 0}

        priority_counts = {}
        type_counts = {}

        for action in actions:
            priority_counts[action.priority.value] = priority_counts.get(action.priority.value, 0) + 1
            type_counts[action.action_type.value] = type_counts.get(action.action_type.value, 0) + 1

        high_priority = priority_counts.get('high', 0)
        if high_priority > 0:
            summary = f"High priority actions required ({high_priority} items)"
        else:
            summary = f"Monitoring and review actions recommended ({len(actions)} items)"

        return {
            "summary": summary,
            "total_actions": len(actions),
            "priority_breakdown": priority_counts,
            "action_type_breakdown": type_counts
        }