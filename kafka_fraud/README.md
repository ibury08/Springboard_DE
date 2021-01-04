Mini-project to create dummy financial transactions, stream them to a Kafka broker, read them into a Kafka consumer, re-send transactions back to different Kafka topics depending on a filter value.

Contains:
- generator/ : creates dummy transactions and sends to kafka broker
- detector/ : consumes transactions from kafka, filters to legit vs. fraudulent transactions, streams to new kafka topics


To run:
`git clone git@github.com:ibury08/Springboard_DE.git && cd Springboard_DE/kafka_fraud`
`docker-compose -f docker-compose.kafka.yml up`
`docker-compose -f docker.compose.yml up`

To see the post-filter topics:
`docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.fraud`
`docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.legit`
