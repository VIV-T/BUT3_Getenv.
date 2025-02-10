# Code pour ecouter et lire les messages
import re
import paho.mqtt.client as paho
# Traitement des img : conversion bytearray en img
from PIL import Image
import io
from traitement_DeepFace import compte_visages_img

# connexion à la BD et execution de requêtes
import psycopg2


# Initialisation de la connexion et creation d'un curseur pour executer des requêtes
connexion = psycopg2.connect(database = "SAE - Analyse et conception outil decisionnel",
                        user = "postgres",
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
curseur = connexion.cursor()



def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    # recuperation des différentes données envoyées sur les différents topics
    topic = re.sub(pattern="[a-z_1-9]+[\/]", repl="", string=msg.topic)

    rpi_id = re.sub(pattern="[\/][a-z_1-9A-Z]+", repl="", string=msg.topic)
    #print(rpi_id)
    data = None

    print(msg.payload)
    if topic != 'byte_array_img' :
        message = msg.payload.decode('utf-8')
    else :
        message = msg.payload
    #print(list(message))

    #message = msg.payload
    table = topic.lower()

    match topic :
        case 'temperature' :
            data = float(message)
        case 'humidity' :
            data = float(message)
        case 'noise' :
            data = float(message)
        case 'isPeopleDetected' :
            data = bool(message)
        case 'TVoC' :
            data = float(message)
        case 'CO2eq' :
            data = float(message)
        case 'alerte_aeration' :
            data = bool(message)
        case 'alerte_intrusion' :
            data = bool(message)
        case 'alerte_incendie' :
            data = bool(message)
        case 'byte_array_img' :
            # Si ce sont des bytearay => les convertir en img + appel de DeepFace
            # recuperation du contenu du msg du topic MQTT
            img_byte_array = message

            # conversion
            image = Image.open(io.BytesIO(img_byte_array))

            # appel de la fonction utilisant DeepFace - recuperation d'un 'int'
            data = compte_visages_img(image)
            # modification du nom du topic pour qu'il corresponde au nom de la table
            table = 'nb_visages'


    # creation et execution de la requête
  
    curseur.execute(f"""
                    INSERT INTO {table}
                    VALUES ('{rpi_id}', {data})
                    """)

    # Les changements deviennent persistants - très important !
    connexion.commit()

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('192.168.220.62', 1883)

liste_id_rpi = [2,3]

for id in liste_id_rpi :
    client.subscribe(f'rpi_{str(id)}/time', qos=1)
    client.subscribe(f'rpi_{str(id)}/temperature', qos=1)
    client.subscribe(f'rpi_{str(id)}/humidity', qos=1)
    client.subscribe(f'rpi_{str(id)}/noise', qos=1)
    client.subscribe(f'rpi_{str(id)}/isPeopleDetected', qos=1)
    client.subscribe(f'rpi_{str(id)}/TVoC', qos=1)
    client.subscribe(f'rpi_{str(id)}/CO2eq', qos=1)
    client.subscribe(f'rpi_{str(id)}/alerte_aeration', qos=1)
    client.subscribe(f'rpi_{str(id)}/alerte_intrusion', qos=1)
    client.subscribe(f'rpi_{str(id)}/alerte_incendie', qos=1)
    # attention, ici on récupère un str(bytearray) et non un bytearray !!!!
    client.subscribe(f'rpi_{str(id)}/byte_array_img', qos=1)

client.loop_forever()

# Fermeture du curseur et de la connexion - (vraiment utile ?)
#cur.close()
#conn.close()