#On importe nos librairies
import time
from rpi_ws281x import Color
from grove.grove_ws2813_rgb_led_strip import GroveWS2813RgbStrip


#Création de l'objet pour le contrôle du composant Grove Stock Led
class GroveLedStick:
	#initialisation de l'objet
	#_pin: numéro de la pin connectée au au module de LEDs
	#_number : nombre de LEDs sur le composant
	def __init__(self, _pin, _number):
		self.number = _number
		self.ledStick = GroveWS2813RgbStrip(_pin, _number)

	#Fonction pour allumer une LED
	#_num : le numéro de la LED à allumer (ATTENTION : la première est à l'indice 0)
	# r : niveau de rouge (0 à 255)
	# g : niveau de vert (0 à 255)
	# b : niveau de bleu (0 à 255)
	def LedRGB_ON(self, num, r, g, b):
		#On configure la LED à allumer
		self.ledStick.setPixelColor(num, Color(r, g, b))
		#On lance la configuration
		self.ledStick.show()
	
	#Fonction pour éteindre une LED
	#_num : le numéro de la LED à allumer (ATTENTION : la première est à l'indice 0)
	def LedRGB_OFF(self, num):
		#On configure la LED à éteindre
		self.ledStick.setPixelColor(num, Color(0,0,0))
		#On lance la configuration
		self.ledStick.show()

	#Fonction pour allumer toutes les LEDs du composant
	# r : niveau de rouge (0 à 255)
	# g : niveau de vert (0 à 255)
	# b : niveau de bleu (0 à 255)
	def LedRGB_AllON(self, r, g, b):
		#On configure la LED à allumer
		for i in range(self.number):
			self.LedRGB_ON(i, r, g, b)
		#On lance la configuration
		self.ledStick.show()

	#Fonction pour éteindre toutes les LEDs du composant
	def LedRGB_AllOFF(self):
		#On configure la LED à éteindre
		for i in range(self.number):
			self.LedRGB_ON(i, 0, 0, 0)
		#On lance la configuration
		self.ledStick.show()

	def LedRGB_N_ON(self, n, r, g, b):
		# On configure la Led a allumer 
		for i in range (n):
			self.LedRGB_ON(i, r,g,b)
		self.ledStick.show()
