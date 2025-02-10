## Installation
# pip install kafka-python
# sudo apt install python3-kafka
from kafka import KafkaConsumer, TopicPartition


## Parametrage du consumer :
# - topic : 'topic_grp_3'
# - server : 'kafka.local'
# - auto_offset_reset : permet de consommer tous les msg historisés dans le topic.
consumer = KafkaConsumer(
    'topic_grp_3',
    bootstrap_servers = "kafka.local",
    auto_offset_reset = "earliest"
)