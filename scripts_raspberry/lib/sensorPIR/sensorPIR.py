#On importe nos librairies
import time
from grove.gpio import GPIO


#Création de l'objet pour le contrôle du composant Grove Adjustable PIR Motion Sensor
class GrovePirMotionSensor:
	#initialisation de l'objet
	#_pinSensor : numéro de la pin connectée au capteur
	def __init__(self,_pinSensor):
		#on initialise la pin reliée au capteur PIR
		self.sensor = GPIO(_pinSensor,GPIO.IN)


	#fonction pour récupérer le status du bouton
	def getSensorValue(self):
		#return 1 : le capteur détecte une présence
		#return 0 : le capteur ne détecte pas de présence
		return self.sensor.read()

