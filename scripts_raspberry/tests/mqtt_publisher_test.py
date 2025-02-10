# Code de publication de messages sur le topic
import paho.mqtt.client as paho
import time

# fonction prend 3 arguments, ils sont nécessaire au foncitonnement du code.
#   client : il s'agit d'une instance de la classe Client() de paho MQTT
#   userdata : les données relatives à l'utilisateur, qui peuvent ne pas être définie
#   mid : Message ID = MID, identifiant unique pour le message (propre au client qui l'emet)
def on_publish(client, userdata, mid):
    print(client)
    print(userdata)
    print("mid: " + str(mid))

client = paho.Client()
client.on_publish = on_publish
client.connect('localhost', 1883)
#client.loop_start()

i = 0
while True:
    i+=1
    (rc, mid) = client.publish('test', "publish from python, msg number : "+str(i), qos=0)
    print('-----')
    print(rc)
    time.sleep(3)

    #client.loop_stop()
