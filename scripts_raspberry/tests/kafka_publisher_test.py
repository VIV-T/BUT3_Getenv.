## Installation
# pip install kafka-python
# sudo apt install python3-kafka
from kafka import KafkaProducer

# bootstrap_servers : identifer le serveur où est déployé Kafka
producer = KafkaProducer(bootstrap_servers = "kafka.local")

# envoi d'un msg
# 'topic_grp_3' permet de preciser le topic ou l'on envoie le msg.
# b'test msg' est le msg envoyé (en byte)    /!\ format 'byte' important, sinon le msg n'est pas envoyé !
# la methode '.get()' permet d'attendre que le msg soit bien envoyé avant de continuer l'execution du code.
producer.send('topic_grp_3', b'test msg').get()
