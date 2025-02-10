#On importe nos librairies
import time
import seeed_dht

#Création de l'objet pour le contrôle du composant Grove Temp&Hum Pro
class GroveDHTSensor:
	#initialisation de l'objet
	#_pinSensor : numéro de la pin connectée au capteur
	def __init__(self,_pinSensor):
		#on initialise le type de capteur utilisé et la pin reliée au capteur
		self.sensor = seeed_dht.DHT("22",_pinSensor) 
		self.humi = 0
		self.temp = 0

	#fonction pour récupérer les valeurs brutes du capteurs
	def getRawSensorValue(self):
		self.humi, self.temp = self.sensor.read()

	#Fonction pour retourner la valeur de l'Humidité
	def humidity(self):
		return self.humi

	#Fonction pour retourner la valeur de la température
	def temperature(self):
		return self.temp


