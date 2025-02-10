#On importe nos librairies
import math
import time
from grove.adc import ADC

#Création de l'objet pour le contrôle du composant Grove Sound Sensor
class GroveSoundSensor:
	#initialisation de l'objet
	#channel : numéro de la pin connectée au capteur
	def __init__(self, channel):
		self.channel = channel
		self.adc = ADC()
                
	#Fonction pour récupérer et retourner la valeur brut du capteur
	def getRawSensorValue(self):
		#(int): ratio, 0(0.0%) - 1000(100.0%)
		self.value = self.adc.read(self.channel)
		return self.value
