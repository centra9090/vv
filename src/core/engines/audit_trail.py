from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

@dataclass
class AuditEntry:
    """Single audit trail entry."""
    timestamp: datetime
    operation: str
    details: Dict[str, Any]
    analysis_id: Optional[str] = None

class AuditTrail:
    """Tracks all operations and decisions for transparency and debugging."""

    def __init__(self):
        self.entries: List[AuditEntry] = []

    def log_operation(self, operation: str, details: Dict[str, Any],
                     analysis_id: Optional[str] = None) -> None:
        """Log an operation with details."""
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc),
            operation=operation,
            details=details,
            analysis_id=analysis_id
        )
        self.entries.append(entry)

    def get_trail(self, analysis_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get audit trail, optionally filtered by analysis ID."""
        if analysis_id:
            filtered_entries = [e for e in self.entries if e.analysis_id == analysis_id]
        else:
            filtered_entries = self.entries

        return [asdict(entry) for entry in filtered_entries]

    def get_operations_summary(self) -> Dict[str, int]:
        """Get summary of operations performed."""
        summary = {}
        for entry in self.entries:
            summary[entry.operation] = summary.get(entry.operation, 0) + 1
        return summary

    def clear_trail(self) -> None:
        """Clear all audit entries."""
        self.entries.clear()