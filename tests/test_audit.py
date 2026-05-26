from src.common.audit import AuditQueue
from src.common.request_context import set_request_id


class TestAuditQueue:
    def setup_method(self):
        self.queue = AuditQueue()
        set_request_id(None)

    def test_enqueue_generates_request_id(self):
        event_id = self.queue.enqueue({"kind": "audit"})
        event = self.queue.get(event_id)
        assert event is not None
        assert event.request_id
        assert event.metadata["request_id"] == event.request_id

    def test_enqueue_preserves_explicit_request_id(self):
        event_id = self.queue.enqueue({"kind": "audit"}, request_id="req-123")
        event = self.queue.get(event_id)
        assert event is not None
        assert event.request_id == "req-123"

    def test_retry_preserves_request_id(self):
        event_id = self.queue.enqueue({"kind": "audit"}, request_id="req-123")
        retry_id = self.queue.retry(event_id, "worker-timeout")
        retry_event = self.queue.get(retry_id)
        assert retry_event is not None
        assert retry_event.request_id == "req-123"
        assert retry_event.metadata["parent_event_id"] == event_id
        assert retry_event.metadata["retry_reason"] == "worker-timeout"

    def test_dead_letter_preserves_request_id(self):
        event_id = self.queue.enqueue({"kind": "audit"}, request_id="req-123")
        assert self.queue.dead_letter(event_id, "max-retries")
        event = self.queue.get(event_id)
        assert event is not None
        assert event.status == "dead_letter"
        assert event.request_id == "req-123"

    def test_batch_publish_preserves_request_id(self):
        first = self.queue.enqueue({"kind": "audit-1"}, request_id="req-1")
        second = self.queue.enqueue({"kind": "audit-2"}, request_id="req-2")
        published = self.queue.batch_publish([first, second])
        assert [item["request_id"] for item in published] == ["req-1", "req-2"]
        assert all(item["metadata"]["request_id"] == item["request_id"] for item in published)
