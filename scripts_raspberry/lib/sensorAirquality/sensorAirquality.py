#On importe nos librairies
import seeed_sgp30
from grove.i2c import Bus

#Création de l'objet pour le contrôle du composant Grove AirQuality
class GroveAirQualitySensor:
	def __init__(self):
		#initialisation de l'objet
		self.sgp30 = seeed_sgp30.grove_sgp30(Bus())
		self.co2_eq_ppm = 0
		self.tvoc_ppb = 0

	#Fonction pour récupérer les valeurs brutes du composant
	def getRawSensorValue(self):
		data = self.sgp30.read_measurements()
		self.co2_eq_ppm, self.tvoc_ppb = data.data

	#Fonction pour retourner le taux de CO2eq
	def CO2eq(self):
		return self.co2_eq_ppm

	#Fonction pour retourner le taux de nano particules TVoC
	def TVoC(self):
		return self.tvoc_ppb
