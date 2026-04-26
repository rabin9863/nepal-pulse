import json
import re
import unicodedata
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
import os

RAW_TOPIC = "raw-news"
PROCESSED_TOPIC = "processed-news"
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKERS", "localhost:9092")


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^\w\s\u0900-\u097F.,!?-]", "", text)
    return text


def process_news_item(item: dict) -> dict:
    cleaned_title = clean_text(item.get("title", ""))
    cleaned_summary = clean_text(item.get("summary", ""))

    return {
        "source": item.get("source", ""),
        "title": item.get("title", ""),
        "cleaned_title": cleaned_title,
        "summary": item.get("summary", ""),
        "cleaned_summary": cleaned_summary,
        "language": item.get("language", ""),
        "category": item.get("category", ""),
        "url": item.get("url", ""),
        "scraped_at": item.get("scraped_at", ""),
        "processed_at": datetime.utcnow().isoformat()
    }


consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="processing-group-v2",
    value_deserializer=lambda x: x.decode("utf-8")
)

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda x: json.dumps(x, ensure_ascii=False).encode("utf-8")
)

print("✅ Processing service is running and listening to raw-news...")

for message in consumer:
    try:
        raw_text = message.value
        raw_item = json.loads(raw_text)

        if not isinstance(raw_item, dict):
            print(f"⚠️ Skipping non-dict message: {raw_text}")
            continue

        processed_item = process_news_item(raw_item)
        producer.send(PROCESSED_TOPIC, processed_item)
        producer.flush()

        print(f"✅ Processed: {processed_item['source']} - {processed_item['cleaned_title']}")

    except json.JSONDecodeError:
        print(f"⚠️ Skipping invalid JSON message: {message.value}")
    except Exception as e:
        print(f"❌ Error processing message: {e}")