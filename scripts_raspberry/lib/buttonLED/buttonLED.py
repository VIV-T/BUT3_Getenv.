#On importe nos librairies
import time
# grove correspond au HAT et gpio correspond aux broches.
# Ainsi, grove.gpio designe les broches du HAT.
from grove.gpio import GPIO


#Création de l'objet pour le contrôle du composant Grove ButtonLED
class GroveButtonLed:
	#initialisation de l'objet
	#_pinButton : numéro de la pin connectée au bouton
	#_pinLed : numéro de la pin connectée à LED
	def __init__(self,_pinButton,_pinLed):
		#on initialise la pin reliée à la LED en sortie
		self.led = GPIO(_pinLed,GPIO.OUT)
		#on initialise la pin reliée au bouton en entrée
		self.button = GPIO(_pinButton,GPIO.IN)


	#fonction pour récupérer le status du bouton
	def getStatusButton(self):
		#return 1 : bouton relâché
		#return 0 : bouton appuyé
		return self.button.read()


	#fonction pour mettre à jour l'état de la LED
	#val = 0 : LED éteinte
	#val = 1 : LED allumé
	def setStatusLed(self,val):
		self.led.write(val)

