from kafka import KafkaProducer
import os
import json
from time import sleep
from transactions import create_random_transaction

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
KAFKA_TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")
TRANSACTIONS_PER_SECOND = float(os.environ.get("TRANSACTIONS_PER_SECOND"))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                             value_serializer=lambda x: json.dumps(x).encode())
    while True:
        transaction: dict = create_random_transaction()
        #message: str = json.dumps(transaction)
        producer.send(KAFKA_TRANSACTIONS_TOPIC, value=transaction)
        print(transaction)
        sleep(SLEEP_TIME)
