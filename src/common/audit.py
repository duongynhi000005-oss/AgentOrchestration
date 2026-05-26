"""Audit event queue with request ID propagation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .request_context import get_request_id


@dataclass
class AuditEvent:
    id: str
    request_id: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "queued"
    attempts: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuditQueue:
    def __init__(self) -> None:
        self._events: Dict[str, AuditEvent] = {}
        self._dead_letters: Dict[str, AuditEvent] = {}

    def enqueue(
        self,
        payload: Dict[str, Any],
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        event_id = str(uuid4())
        resolved_request_id = request_id or get_request_id() or str(uuid4())
        event = AuditEvent(
            id=event_id,
            request_id=resolved_request_id,
            payload=dict(payload),
            metadata=dict(metadata or {}),
        )
        event.metadata.setdefault("request_id", resolved_request_id)
        self._events[event_id] = event
        return event_id

    def get(self, event_id: str) -> Optional[AuditEvent]:
        return self._events.get(event_id) or self._dead_letters.get(event_id)

    def retry(self, event_id: str, reason: str) -> Optional[str]:
        event = self._events.get(event_id) or self._dead_letters.get(event_id)
        if not event:
            return None
        retry_id = str(uuid4())
        retry_event = AuditEvent(
            id=retry_id,
            request_id=event.request_id,
            payload=dict(event.payload),
            metadata={
                **event.metadata,
                "parent_event_id": event.id,
                "retry_reason": reason,
            },
            attempts=event.attempts + 1,
        )
        retry_event.metadata["request_id"] = event.request_id
        self._events[retry_id] = retry_event
        return retry_id

    def dead_letter(self, event_id: str, reason: str) -> bool:
        event = self._events.pop(event_id, None)
        if not event:
            return False
        event.status = "dead_letter"
        event.metadata = {**event.metadata, "dead_letter_reason": reason, "request_id": event.request_id}
        self._dead_letters[event_id] = event
        return True

    def batch_publish(self, event_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        ids = event_ids or list(self._events.keys())
        published: List[Dict[str, Any]] = []
        for event_id in ids:
            event = self._events.get(event_id)
            if not event:
                continue
            event.status = "published"
            event.metadata["request_id"] = event.request_id
            published.append(self._serialize(event))
        return published

    def snapshot(self) -> Dict[str, Any]:
        return {
            "queued": [self._serialize(event) for event in self._events.values()],
            "dead_letters": [self._serialize(event) for event in self._dead_letters.values()],
        }

    @staticmethod
    def _serialize(event: AuditEvent) -> Dict[str, Any]:
        return {
            "id": event.id,
            "request_id": event.request_id,
            "payload": dict(event.payload),
            "metadata": dict(event.metadata),
            "status": event.status,
            "attempts": event.attempts,
            "created_at": event.created_at,
        }
