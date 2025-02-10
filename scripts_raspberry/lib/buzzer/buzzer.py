#On importe nos librairies
import time
from grove.factory import Factory

#Création de l'objet pour le contrôle du composant Grove Buzzer
class GroveBuzzer:
	#initialisation de l'objet
	#_pinButton : numéro de la pin connectée au Buzzer
	def __init__(self,_pin):

		self.buzzer = Factory.getGpioWrapper("Buzzer",_pin)

	#Fonction pour activer le Buzzer
	def on(self):
		self.buzzer.on()
		#time.sleep(0.1)
	
	#Fonction pour désactiver le Buzzer
	def off(self):
		self.buzzer.off()

