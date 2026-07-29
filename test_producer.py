from generator.producer import ClickstreamProducer

producer = ClickstreamProducer()

event = {
    "customer_id": "C1001",
    "session_id": "S001",
    "event_type": "product_view",
    "product_id": "P101",
    "price": 999.99,
    "timestamp": "2026-07-29T12:30:00"
}

producer.send_event(event)