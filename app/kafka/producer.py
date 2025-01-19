from kafka import KafkaProducer
import json
from datetime import datetime
from bson import ObjectId  # Importa o ObjectId do MongoDB
# Função para serializar objetos datetime e ObjectId
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converte datetime para string ISO
    elif isinstance(obj, ObjectId):
        return str(obj)  # Converte ObjectId para string
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")
def create_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',  # Endereço do Kafka no Docker
        value_serializer=lambda v: json.dumps(v, default=custom_serializer).encode('utf-8')  # Usa a função customizada para serialização
    )
    return producer
def send_event(event_data):
    producer = create_kafka_producer()
    # Envia o evento para o tópico 'appointments'
    producer.send('appointments', value=event_data)
    producer.flush()  # Garante que todos os eventos sejam enviados antes de terminar